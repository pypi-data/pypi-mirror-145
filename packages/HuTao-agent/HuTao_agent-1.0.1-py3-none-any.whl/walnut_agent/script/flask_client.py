# -*- coding: utf-8 -*-

# @File    : flask_client.py
# @Date    : 2022-02-08
# @Author  : chenbo

__author__ = 'chenbo'

import argparse
import threading
import time
import sys
from loguru import logger

from flask import Flask, request, jsonify, Response
from fast_dict import Dictionary

from walnut_agent.common import do_monkeylog, do_json
from walnut_agent.script.agent import iOS_monkey_start, iOS_monkey_shutdown
from walnut_agent.script.util_handle import route, setting
from walnut_agent.script import http_handle, agent
from walnut_agent.script.app_handle import tid, add
from typing import Any


def respModel(result, isCheck=True):
    if str(result).find("失败") != -1 and isCheck is True:
        return do_json.dumps({"code": "8020", "msg": None, "success": False, "result": result, "tid": None, "ext": None})
    else:
        return do_json.dumps({"code": "8000", "msg": None, "success": True, "result": result, "tid": None, "ext": None})


class JsonResponse(Response):

    @classmethod
    def force_type(
            cls, response: "Response", environ=None
    ) -> "JsonResponse":
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)


class FlaskApp(Flask):

    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

    def run(
            self,
            host: str = None,
            port: int = None,
            debug: bool = None,
            load_dotenv: bool = True,
            **options: Any,
    ) -> None:
        self._activate_background_job(host, port)
        super().run(host, port, debug, load_dotenv, **options)

    def _activate_background_job(self,
                                 host: str = None,
                                 port: int = None,
                                 ):
        """
        连接主服务器 heartbeat
        """

        def run_job():
            time.sleep(3)
            http_handle.master_service.join_client(host, port, setting.agent.name)

        t1 = threading.Thread(target=run_job)
        t1.start()


app = FlaskApp(__name__)
app.response_class = JsonResponse
app.config["JSON_AS_ASCII"] = False

connected = {
    "ios": ''
}


@app.route('/', methods=["GET"])
def home():
    """
    返回所有接口的简易信息
    """
    data = Dictionary({
        "local": setting.agent.ip,
        "path": Dictionary({
            "root": route.BASE_DIR.__str__(),
            "script": route.SCRIPT_PATH.__str__(),
            "log": route.LOG_PATH.__str__(),
            "report": route.REPORT_PATH.__str__(),
            "export": route.EXPORT_PATH.__str__()
        }),
        "api": [
            {
                "path": "/runner",
                "args": {
                    "task": "int"
                },
                "help": "执行任务"
            },
            {
                "path": "/udid",
                "args": {
                },
                "help": "获取已连接状态的设备id"
            }
        ]
    })
    return data


@app.route('/runner', methods=["GET"])
def runner():
    """
    执行任务
    参数: task: int  任务id
    """
    data = Dictionary({
        "succeed": True,
        "msg": "",
        "data": None
    })
    if request.args is None:
        data["succeed"] = False
        data["msg"] = "请输入需要运行的任务id"
    else:
        task: str = request.args.to_dict().setdefault("task", None)
        data["data"] = agent.run_task(task_id=task)
    return data


@app.route('/udid', methods=["GET"])
def udid():
    """
    获取已连接状态的设备id
    """
    state = http_handle.wda_state.state()
    data = Dictionary({
        "iOS": tid.get_info(),
        "Android": add.get_info(),
        "ios_connected": connected["ios"] if state else ''
    })
    return respModel(data)


@app.route('/start_wda', methods=["GET"])
def start_wda():
    data = Dictionary({
        "msg": "请求成功"
    })
    if request.args is None:
        data["msg"] = "参数udid不能为空"
    else:
        req: dict = request.args.to_dict()
        udid: str = req.setdefault("udid", None)
        if udid and udid in tid.get_devices():
            connected["ios"] = udid
            data["msg"] = agent.iOS_wda_start(udid)
        else:
            data["msg"] = "设备不存在或未连接"
    return data


@app.route('/ios_monkey', methods=["GET"])
def ios_monkey():
    udid = request.args.get("udid")
    appid = request.args.get("appid")
    duration = request.args.get("duration")
    throttle = request.args.get("throttle")
    yppno = request.args.get("yppno")
    tester = request.args.get("tester")
    monkey_msg = iOS_monkey_start(udid, appid, duration, yppno, tester, throttle)
    return respModel(monkey_msg)


@app.route('/ios_monkey_shutdown', methods=["GET"])
def ios_monkey_shutdown():
    thread_id = request.args.get("thread_id")
    record_id = request.args.get("record_id")
    monkey_msg = iOS_monkey_shutdown(record_id, thread_id)
    return respModel(monkey_msg)


@app.route('/end_wda', methods=["GET"])
def end_wda():
    data = Dictionary({
        "msg": "请求成功"
    })
    tid.end_wda()
    connected["ios"] = ''
    return data


@app.route('/status_wda', methods=["GET"])
def status_wda():
    state = http_handle.wda_state.state()
    data = Dictionary({
        "state": state
    })
    return data


@app.route('/ios_info', methods=["GET"])
def ios_info():
    data = Dictionary({
        "list": tid.get_info()
    })
    return data


@app.route('/collect_ios_monkey_log', methods=["GET"])
def collect_ios_monkey_log():
    record_id = request.args.get("record_id")
    return respModel(do_monkeylog.collect_ios_monkey_log(record_id))


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        '-D', '--debug', dest='debug', action='store_true',
        help="show version")

    args = parser.parse_args()

    if args.version:
        from ..__about__ import __version__
        msg = f"HuTao Version:{__version__}"
        print(msg)
        exit(0)

    log_file = route.BASE_DIR / 'runtime' / 'agent{time}.log'
    # 日志等级从低到高的顺序是: DEBUG < INFO < WARNING < ERROR < CRITICAL
    config = {
        "handlers": [
            {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
             "backtrace": True,
             "level": 'WARNING',
             "diagnose": True},
            # 输出日志到文件
            # rotation 滚动日志大小，retention 日志的保留时长, compression 文件压缩格式, serialize 日志序列化为JSON
            {"sink": log_file,
             "backtrace": True,
             "serialize": False,
             "rotation": "500 MB", "retention": "3 days", "compression": "zip"},
        ],
        "extra": {"user": "someone"}
    }
    logger.configure(**config)

    # 开启debug模式
    flask_debug = False
    if args.debug:
        flask_debug = True

    # 上报IP和端口到master服务器
    app.run(
        host="0.0.0.0",
        port=setting.agent.port,
        debug=flask_debug
    )


if __name__ == '__main__':
    main()
