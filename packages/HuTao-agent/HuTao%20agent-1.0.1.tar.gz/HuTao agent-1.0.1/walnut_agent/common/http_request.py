#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from walnut_agent.common.config import proxies
from loguru import logger


class HttpRequest:
    def __init__(self, preUrl='', isProxy=False):
        self.session = requests.Session()
        self.preUrl = preUrl
        self.isProxy = isProxy

    def request(self, method, url, data=None, **kwargs):
        method = method.upper()  # 将字符转成全部大写
        url = self.preUrl + url
        if data is not None and type(data) == str:
            data = eval(data)  # 如果是字符串就转成字典
        logger.debug('method: {0}  url: {1}'.format(method, url))
        logger.debug('data: {0}'.format(data))
        try:
            if method in ["GET", "POST"]:
                if not self.isProxy:
                    resp = self.session.request(method, url, data, **kwargs)
                else:
                    resp = self.session.request(method, url, data, proxies=proxies, **kwargs)
                logger.debug('response: {0}'.format(resp.text))
                return resp
            else:
                logger.error('Un-support method !!!')
        except requests.exceptions.SSLError as e:
            msg = "发送HTTP请求时遇到SSL相关错误:{0}".format(e)
            logger.error(msg)
            return msg

    def close(self):
        self.session.close()  # 关闭session


if __name__ == '__main__':
    pass
