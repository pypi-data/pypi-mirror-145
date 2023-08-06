# -*- coding: utf-8 -*-

# @File    : agent.py
# @Date    : 2022-01-25
# @Author  : chenbo

"""
agent 客户端启动程序
"""

__author__ = 'chenbo'

import ctypes
import threading
import time
from typing import List

from walnut_agent import ios_monkey
from walnut_agent.common import config, do_monkeylog
from walnut_agent.common.do_db import DataOp, dbname
from walnut_agent.common.mail import Mail
from walnut_agent.script.app_handle import AppHandle, AdbHandle, TidHandle, tid
from walnut_agent.script.case_class import Platform, Feature
from walnut_agent.script.runner import Runner
from loguru import logger


# 通过任务id执行master下发的测试任务
def run_task(task_id: str) -> str:
    # 组装
    runner = Runner(task_id)
    runner.start()
    return runner.tag


# 获取设备号列表
def get_udid(platform: Platform) -> List[str]:
    udid = []
    app: AppHandle = None
    if platform == Platform.Android:
        app = AdbHandle()
    elif platform == platform.ios:
        app = TidHandle()
    # 重试3次
    for i in range(3):
        udid = app.get_devices()
        if len(udid) > 0:
            return udid
    return udid


def iOS_wda_start(udid: str) -> str:
    tid.switch_serial(udid)
    is_installed = tid.install_wda()
    if is_installed:
        return tid.start_wda(udid)
    else:
        return "WebDriverAgent start failed"


def iOS_monkey_start(udid, appid, target_time, yppno, tester, throttle):
    if throttle == "":
        throttle = 300
    with DataOp() as db:
        # 检测tester是否在表中
        result = db.fetchOne("SELECT username FROM {0}.auth_user WHERE username='{1}'".format(dbname, tester))
    if result == 0:
        return "该用户没有数据存档，请检查域账号的拼写。首次使用时，请先用该账号[{0}]登录一次tdp.yupaopao.com！"
    monkey = ios_monkey.SpiderMonkeyIOS(udid, appid)
    if isinstance(monkey.device, str):
        msg = monkey.device
    else:
        is_installed = monkey.install_runner()
        if is_installed == 1:
            device_info = monkey.getDeviceInfo()
            if isinstance(device_info, str):
                msg = device_info
            else:
                msg = "连接成功，正在运行monkey，请耐心等待"
                try:
                    app_info = monkey.getAppInfo()
                except TypeError:
                    msg = "[{0}]获取app信息失败，请检查是否安装了[{1}]".format(device_info["phone_name"], monkey.app_name)
                    logger.warning(msg)
                else:
                    thr = threading.Thread(target=monkey.runMonkey,
                                           args=(target_time, device_info, app_info, tester, yppno, throttle))
                    thr.start()
        else:
            msg = is_installed
    return msg


def iOS_monkey_shutdown(record_id, thread_id):
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(int(thread_id)), ctypes.py_object(SystemExit))
    with DataOp() as db:
        sql = "SELECT phone_nameFROM {0}.test_record_ios WHERE record_id={1}".format(dbname, record_id)
        result = db.fetchOne(sql)
        phone_name = result["phone_name"]
        if res == 0:
            msg = "设备[{0}]终止测试失败，线程id错误！".format(phone_name)
            kv = {"run_status": 6}
        elif res != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            msg = "设备[{0}]终止测试失败，线程状态设置失败！".format(phone_name)
            kv = {"run_status": 6}
        else:
            msg = "设备[{0}]终止测试成功！".format(phone_name)
            end_time = time.strftime("%Y-%m-%d %H:%M:%S")
            kv = {"run_status": 2, "end_time": end_time}
        db.update("test_record_ios", kv, "record_id={0}".format(record_id))
    return msg


# def iOS_monkey_mail(record_id, receivers):
#     sql = "SELECT {0} FROM {1}.test_record_ios where record_id={2};".format(str(config.test_record_cols)[1:-1].
#                                                                             replace("'", ""), dbname, record_id)
#     with DataOp() as db:
#         result = db.fetchOne(sql)
#     if not result:
#         return "发送邮件失败，数据库中没有相关记录！"
#     mail_content = "测试人员：{0}\r预期运行时长：{1}分钟\r实际运行时长：{2}分钟\r运行状态：{3}\r运行时间：{4} - {5}\r事件覆盖率：" \
#                    "{6}\r\r设备信息：\r设备名称：{7}\r手机型号：{8} {9}\r系统版本：{10}\r\rapp信息：\r版本号：{11}\rbuild_id：" \
#                    "{12}".format(result["tester"], result["target_time"], result["duration"], result["run_status"],
#                                  result["begin_time"], result["end_time"], "IOS暂不支持获取时间覆盖率",
#                                  result["phone_name"], result["phone_brand"], result["phone_type"], result["phone_sys"],
#                                  result["version_name"], result["version_code"])
#     # 防止中途bug_number未能正常写入时，邮件文本中的bug_number错误
#     if result["bug_number"] and result["bug_number"] != "[]":
#         bug_number = result["bug_number"].split(",")
#         bug_urls = str(["http://jira.yupaopao.com/browse/" + bug_url for bug_url in bug_number]).replace(",", "\r")
#         bug_urls = do_monkeylog.listToStr(bug_urls)
#         mail_content += "\rbug列表：\r{0}".format(bug_urls)
#     # 发送测试报告邮件
#     return Mail().sendMail(mail_content, receivers)


def init_environment():
    """
    初始化环境
    """
    pass


if __name__ == '__main__':
    iOS_wda_start("679c48afa066538330baad04892da34b5264bf55")
