# -*- coding: utf-8 -*-

# @File    : ws_client.py
# @Date    : 2022-01-24
# @Author  : chenbo

# 用于链接 websokect 的客户端

__author__ = 'chenbo'

import websocket
from threading import Thread
from queue import Queue
from loguru import logger

from walnut_agent.script.util_handle import setting


class WsClient(Thread):

    def __init__(self):
        super(WsClient, self).__init__()
        self.queue: Queue = Queue()
        self._ws: websocket.WebSocketApp = None

    def send(self, msg):
        logger.debug(f'发送消息:{msg}')
        if self._ws.sock:
            self._ws.send(msg)

    def run(self):
        websocket.enableTrace(True)
        self._ws = websocket.WebSocketApp(f"{setting.app.ws_host}/ws/task/1/",
                                          on_open=self._on_open,
                                          on_message=self._on_message,
                                          on_error=self._on_error,
                                          on_close=self._on_close)
        self._ws.run_forever()

    def _on_message(self, ws, message):
        self.queue.put(message)

    @staticmethod
    def _on_error(self, ws, error):
        logger.error(f"websocket连接异常:{error}")

    def _on_close(self, ws):
        pass

    def _on_open(self, ws):
        pass
