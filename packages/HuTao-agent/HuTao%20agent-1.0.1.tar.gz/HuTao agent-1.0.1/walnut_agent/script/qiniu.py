# -*- coding: utf-8 -*-

# @File    : qiniu.py
# @Date    : 2022-03-07
# @Author  : chenbo

__author__ = 'chenbo'


# def uploadFiles(path, date=""):
#     url = 'https://test-cdn.hibixin.com'
#     body = {'bizType': "log_stream_storage", "fileType": 4}
#
#     with open(log_path, mode="r", encoding="utf-8") as f:
#         file = {"file": (log_path, f)}
#         resp = do_json.loads(hr.request("POST", "/cdn/backStage/upload", data=body, files=file).text)["result"]["url"]
#         return resp
