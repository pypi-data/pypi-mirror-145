#!/usr/bin/env python
# coding: utf-8

import contextvars
import uuid

class Helper(object):
    """
    辅助基类模块
    """

    def __init__(self):
        self._config = dict()


        self._partition = 0
        # 发送消息的状态，True 是成功发送，False 是发送失败
        self._send_error = None
        self._send_msg = None
        self._message_context =None

    def config_servers(self, url:str):
        """
        配置连接的服务器,如['localhost:9092']
        """
        self._config["url"] = f'pulsar://{url}'
        return self

    def config_tenant(self, tenant:str):
        """ 配置租户 """
        self._config["tenant"] = tenant
        return self

    def config_namespace(self, namespace:str):
        """ 配置命名空间 """
        self._config["namespace"] = namespace
        return self

    def set_message_id(self,message_id):
        """
        设置消息id
        """
        if self._message_context is None:
            self._message_context= contextvars.ContextVar('message id')
        self._message_context.set(message_id)

    def get_message_id(self):
        """返回消息id"""
        try:
            return self._message_context.get()
        except Exception as e:
            str(uuid.uuid4())