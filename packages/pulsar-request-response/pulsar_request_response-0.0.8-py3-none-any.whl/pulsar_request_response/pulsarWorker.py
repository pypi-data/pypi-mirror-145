#!/usr/bin/env python
# encoding: utf-8
from .kafkapacket_pb2 import KafkaPacket
from .producer_helper import ProducerHelper
from .consumer_helper import ConsumerHelper
from .publishesMessage import PublishesMessage
from .workerDelegate import WorkerDelegate
from typing import Optional, Dict, List, Any
import asyncio
import traceback
import uuid
import time
import logging
import pulsar
import contextvars
import json



logger = logging.getLogger(__name__)


class PulsarWorker(object):
    """ 
    """

    def __init__(self,
                 host: str,
                 tenant: str,
                 namespace:str = "",
                 private_topic: str = "",
                 auth_token: str = "",
                 is_debug = False,
                 ):
        """

        :params host pulsar 集群节点
        :params private_topic 私人topic，用于发送信息后接收响应的信息
        """
        self._message_context = contextvars.ContextVar('message id')
        logger.info("pulsar worker init.")
        host = f'pulsar://{host}'
        self._tenant = tenant
        self._namespace = namespace
        if auth_token :
            from pulsar import AuthenticationToken
            self._client = pulsar.Client(host, authentication=AuthenticationToken(auth_token))
                 
        else:
            self._client = pulsar.Client(host)

        if private_topic !="":
            private_topic = f"{tenant}/{namespace}/{private_topic}"
        else:
            private_topic =  f"{tenant}/{namespace}/{str(uuid.uuid4())}"

        self._producer = ProducerHelper()
        self._producer._client = self._client
        self._producer._message_context=self._message_context
        self._producer.config_servers(host)
        self._producer.config_tenant(tenant)
        self._producer.config_namespace(namespace)

        self._consumer = ConsumerHelper()
        self._consumer._client = self._client
        self._message_context=self._message_context
        self._consumer.config_servers(host)
        self._consumer.config_tenant(tenant)
        self._consumer.config_namespace(namespace)

        # 发出信息后，等待响应的信息列表
        self._wait_response_message: Dict[str, PublishesMessage] = {}
        # 注册接收指定topic 的消费者
        self._consumer_registers: Dict[str, callable] = {}
        # 如果指定routingKey，就使用topic+routingKey实现分发方法。(在这里routingKey和method都是用于分发调用业务方法，可认为是等价)
        self._method_registers: Dict[str,callable] = {}
        # 因为可能会往一些没有存在是topic发送信息，所以需要正式发送前发送hello 信息
        self._register_topic: Dict[str, int] = {}

        self._private_topic = private_topic
        # self._private_topic = str(uuid.uuid4())

        self.event_loop = asyncio.get_event_loop()

        # self._register_private_topic()
        self._open_private_topic()
        if is_debug:
            self._consumer.open_debug()


    async def _on_message(self, message: KafkaPacket):
        """ 
        当接收到kafka 信息的时候会触发调用这个方法
        分两种情况，1 发送的信息后收到的回复 2 接收到新信息
        """
        logger.debug("_on_message, _wait_response_message length:{}".format(self._wait_response_message))
        logger.debug(message)
        if message.correlationId in self._wait_response_message:
            # 发送信息后收到的回复
            publish_message = self._wait_response_message[message.correlationId]
            del self._wait_response_message[message.correlationId]
            logger.debug(
                "response msg.correlationId, msg.body: {0}, {1}".format(message.correlationId, message.body))
            # publish_message.callback(message)
            worker_delegate = WorkerDelegate(publish_message.callback, message, self._private_topic)
            await worker_delegate.executor()
        else:
            # 接收到新的信息后查询处理方法，如果没有注册，则丢弃
            if message.sendTo in self._consumer_registers:
                deal_function = self._consumer_registers[message.sendTo]
                if message.routingKey:
                    key = "{0}-{1}".format(message.sendTo,message.routingKey)
                    if key in self._method_registers:
                        deal_function = self._method_registers[key]

                worker_delegate = WorkerDelegate(deal_function, message, self._private_topic)
                response_publish_message = await worker_delegate.executor()
                # 查询信息中包含的是否需要回复消息，没有replyTo即不需要，就不发送回复信息
                if message.replyTo:
                    self._send_message(response_publish_message)

    def _send_message(self, message):
        """ 
        发送信息
        """
        self._register_private_topic()
        if isinstance(message, PublishesMessage):
            
            value = message.to_protobuf()
            is_reply = message.is_reply
            need_reply = True if message.reply_to else False
            if not message.send_to in self._register_topic:
                self._register_topic[message.send_to] = 1
            if value.body:
                self._producer.send(value,message.send_to)
                logger.debug("_send_message: {}".format(message.to_dict()))
                if not is_reply and need_reply:
                    self._wait_response_message[message.correlation_id] = message
        else:
            
            if not message.sendTo in self._register_topic:
                self._open_topic(message.sendTo)
                self._register_topic[message.sendTo] = 1
            if message.body:
                
                self._producer.send(message,message.send_to)
                logger.debug("_send_message: {}".format(message))

    async def _bind_to_on_message(self, value,properties=None):
        """ 
        绑定消费者收到信息后调用 _on_message
        """
        if value is None:
            return
        logger.debug("_bind_to_on_message: {}".format(value))
        try:
            packet = KafkaPacket()
            packet.ParseFromString(value)
            await self._on_message(packet)
        except Exception as e:
            logger.exception(traceback.format_exc())
            logger.exception(e)
            logger.error(f'properties:{properties}')
            if properties is not None and properties.get("replyTo"):
                replyTo= properties.get("replyTo")
                error_response = {
                    "code":-1,
                    "message":str(e)
                }
                await self.send(replyTo,json.dumps(error_response).encode('utf-8'),
                            content_type=properties.get('contentType'),
                            message_id=properties.get('messageId')
                            )

    def subscribe(self, topic: str,subscription_name:str, work: callable,routingKey=""):
        """ 
        订阅主题
        """
        if self._tenant not in topic:
            topic =f"{self._tenant}/{self._namespace}/{topic}"

        logger.debug("subscribe topic: {}".format(topic))
        if topic not in self._consumer_registers:
            self._consumer.receive_async(topic, subscription_name,self._bind_to_on_message)
            self._consumer._loop.call_later(0.01,self._consumer._loop.create_task,self._consumer._poll_task())

            self._consumer_registers[topic] = work
        key = "{0}-{1}".format(topic,routingKey)

        if key not in self._method_registers:
            self._method_registers[key] =work
    
    def _open_topic(self, topic):
        """ 
        多次发送保障打开通道
        """

    def _open_private_topic(self):
        """ 
        多次发送保障打开通道
        """
            #asyncio.sleep(0.01)        

    def _register_private_topic(self):
        """ 
        注册私密的topic,用于发送信息后接收到信息
        """
        if self._private_topic == "":
            return
        if self._private_topic not in self._consumer_registers:
            self._open_topic(self._private_topic)
        subscription_name = str(uuid.uuid4())
        self.subscribe(self._private_topic,subscription_name, lambda no_use: no_use)

    async def send(self, topic: str,
                   message: bytes,
                   content_type: str = None,
                   content_encoding: str = 'utf-8',
                   group_id: str = '0',
                   message_id: str = None,
                   msg_type: str = None,
                   user_id: str = None,
                   app_id: str = None,
                   headers: dict = None,
                   need_reply: bool = True, 
                   routing_key: str = None
                   ):
        """ 
        发送信息
        """
        logger.info("send message: {}".format(message))
        waiter = self.event_loop.create_future()

        def for_callback(response):
            waiter.set_result(response)
            return waiter.result()
        
        reply_to = self._private_topic if need_reply else None


        publish_message = PublishesMessage(
            payload=message,
            reply_to=reply_to,
            send_to=topic,
            correlation_id="",
            content_type=content_type,
            content_encoding=content_encoding,
            group_id=group_id,
            message_id=message_id,
            msg_type=msg_type,
            user_id=user_id,
            app_id=app_id,
            headers=headers,
            callback=for_callback,
            routing_key=routing_key
        )
        publish_message.new_correlation_id()
        self._send_message(publish_message)
        if not need_reply:
            return
        await self._consumer.poll_task()
        return await waiter

    def stop_consumer(self, topic: str):
        """ 
        停止接收数据
        """
        self._consumer.stop_consumer([topic])
        del self._consumer_registers[topic]
