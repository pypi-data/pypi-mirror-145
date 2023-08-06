#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http 请求
"""

__author__ = 'chenbo'

import time
from pathlib import Path

import requests
from loguru import logger

from walnut_agent.common import config
from walnut_agent.script.util_handle import setting
from walnut_agent.script.case_class import Platform


class HttpHandle(requests.Session):

    def __init__(self):
        super(HttpHandle, self).__init__()

    def request(self, method, url, name=None, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method:
            method for the new :class:`Request` object.
        :param url:
            URL for the new :class:`Request` object.
        :param name: (optional)
            Placeholder, make compatible with Locust's HttpSession
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        # timeout default to 120 seconds
        kwargs.setdefault("timeout", 120)

        # set stream to True, in order to get client/server IP/Port
        kwargs["stream"] = True

        start_timestamp = time.time()
        response = requests.Session.request(self, method, url, **kwargs)
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)

        logger.info(
            f"request: {method}: {url}, "
            f"status_code: {response.status_code}, "
            f"response_time(ms): {response_time_ms} ms, "
        )

        return response


class MasterService(HttpHandle):
    """
    远程服务器接口操作
    """
    # 远程服务器域名
    root = setting.app.http_host

    def __send__(self, url: str, json: dict) -> dict:
        """
        为请求设置默认参数
        """
        url = url if url.startswith('/') else f'/{url}'
        try:
            response = self.request(method='POST', url=f'{self.root}{url}', json=json).json()

            if response["code"] != 8000:
                logger.error(response["msg"])
                return dict()

            return response
        except Exception as e:
            logger.error(f"HuTao 远程请求失败: {e.args}")
            return None

    def task_get(self, _id: int) -> dict:
        """
        获取任务信息
        """
        data = self.__send__('/task/get/', {"id": str(_id)})['data']
        config.remote_info["platform"] = data['platform']
        config.remote_info["devices"] = data['devices']
        data['platform'] = Platform.match(data['platform'])
        return data

    def task_running(self, _id: int, tag: str) -> dict:
        """
        设置任务为运行中状态
        """
        return self.__send__('/task/running/', {
            "id": str(_id),
            "agent_ip": setting.agent.ip,
            "agent_port": setting.agent.port,
            "tag": tag,
        })

    def task_finish(self, _id: int, report: str, tag: str) -> dict:
        """
        设置任务为运行完成状态，并上传报表路径
        """
        return self.__send__('/task/finish/', {
            "id": str(_id),
            "report": report,
            "agent_ip": setting.agent.ip,
            "agent_port": setting.agent.port,
            "tag": tag,
        })

    def download(self, url: str, path: Path) -> Path:
        """
        下载文件
        """
        url = url if url.startswith('/') else f'/{url}'
        f = requests.get(f'{self.root}/ht{url}')
        with path.open('wb+') as file:
            file.write(f.content)
        return path

    def upload_log(self, file_path: Path) -> dict:
        """
        上传日志和报表
        """
        url = '/task/upload_log/'
        file = Path(file_path)
        data = {}
        with file.open('rb') as f:
            data['file'] = (file.name, f.read())
        from urllib3 import encode_multipart_formdata
        formdata = encode_multipart_formdata(data)
        res = requests.post(f'{self.root}{url}', headers={'Content-Type': formdata[1]}, data=formdata[0])
        return res.json()

    def join_client(self, ip: str, port: str, name: str = None) -> None:
        """
        连接主服务器
        """
        self.__send__('/task/agent_joint/', {
            "ip": ip,
            "port": port,
            "agent_name": name
        })


master_service: MasterService = MasterService()


class _WdaState(HttpHandle):

    def state(self) -> bool:
        try:
            import wda
            c = wda.Client('http://localhost:8200')
            print(c.info)

            return True if c.info else False
        except Exception:
            return False


wda_state: _WdaState = _WdaState()


class _QiNiu(HttpHandle):
    root = "https://test-cdn.hibixin.com"

    def __send__(self, url: str, method: str = 'POST', json: dict = None, files: dict = None) -> dict:
        url = url if url.startswith('/') else f'/{url}'
        try:
            response = self.request(method=method, url=f'{self.root}{url}', json=json, timeout=1000, files=files).json()
            return response
        except Exception as e:
            logger.error(f"七牛 远程请求失败: {e.args}")
            return None

    def uploadFiles(self):
        """
        Body
        /**
         * 文件
         */
        private MultipartFile file;

        /**
         * 业务类型，用来区分业务，不同业务有不同的上传处理逻辑
         * com.yupaopao.platform.material.constant.BusinessTypeEnum
         */
        private String bizType;

        /**
         * 文件类型
         * com.yupaopao.platform.material.constant.FileTypeEnum
         */
        private int fileType;


        Response:
        /**
         * 域名
         */
        private String domain;

        /**
         * url
         */
        private String url;

        /**
         * hash
         */
        private String hash;

        /**
         * key
         */
        private String key;

        /**
         * 文件大小
         */
        private long fsize;

        /**
         * 宽度
         */
        private String width;

        /**
         * 高度
         */
        private String height;

        /**
         * 附加返回值
         */
        private Map<String, Object> attachment;
        """
        self.__send__('/cdn/backStage/upload',
                      json={
                          'bizType': "log_stream_storage",
                          "fileType": 4
                      },
                      files={}
                      )


if __name__ == '__main__':
    print(wda_state.state())
