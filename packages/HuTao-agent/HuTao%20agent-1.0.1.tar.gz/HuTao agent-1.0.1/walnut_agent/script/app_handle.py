#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
同步操作的adb shell 或 ideviceinfo 命令
"""

__author__ = 'chenbo'

import asyncio
import os
import platform
import signal
import subprocess
import time
import select
import traceback
from pathlib import Path
from typing import List, Union, Any
from queue import Queue

import tidevice

try:
    import msvcrt
    import _winapi

    _mswindows = True
except ModuleNotFoundError:
    _mswindows = False
    import _posixsubprocess

    import selectors

from walnut_agent.common import config
from walnut_agent.script.case_class import Feature
from loguru import logger
from walnut_agent.script.util_handle import setting
import threading
from tidevice import Device, Usbmux, _relay
from adbutils import adb, AdbTimeout, AdbDevice


def process_cmd(shell: str, **kwargs) -> subprocess.Popen:
    """统一生成subprocess.Popen"""
    formats = 'gbk' if config.run_platform == "Windows" else 'utf-8'
    return subprocess.Popen(shell,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True, close_fds=True,
                            cwd=config.BASE_DIR,
                            encoding=formats,
                            start_new_session=True,
                            **kwargs)


# MAC系统失眠
def caffeinate_Mac(time):
    shell = "caffeinate -t " + time
    result = subprocess.run(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                            check=True)
    print(result)
    return result


class CmdThread(threading.Thread):
    """
    多线程执行的终端命令行操作
    """

    def __init__(self, shell: str, timeout: int, line_count: int = 100):
        super(CmdThread, self).__init__()
        self.timeout: int = timeout
        self.line_count: int = line_count
        self.shell: str = shell
        self.process: subprocess.Popen = None
        self.queue: Queue = Queue()

    def run(self):
        print(f'CmdThread: {threading.current_thread()}')
        msg = "[INFO]开始执行: %s" % self.shell
        logger.info(msg)
        self.process = process_cmd(self.shell)
        # 初始化继续flag
        continue_flag = True
        # 初始化执行结果信息
        msg = "[SUCCESS]执行成功！！！"
        index = 0
        try:
            last_line_received = time.time()
            while continue_flag:
                last_line_received = time.time()
                line = self.process.stdout.readline()
                line = line.strip()
                if line:
                    logger.info(line)
                    self.queue.put(line)
                if self.process.poll() is not None:
                    if index > 100:
                        continue_flag = False
                    index += 1
            if continue_flag:
                if self.process.returncode:
                    msg = "[FAIL]p.returncode为1，执行异常终止，需要确认异常原因"
        except subprocess.TimeoutExpired:
            msg = f"[FAIL]超时异常: 执行 {self.shell} 超时"
        except Exception as e:
            tb = traceback.format_exc()
            msg = f"[FAIL]未知异常 : {str(tb)}"
        logger.info(msg)

    def kill_process(self):
        """关闭process对象"""
        if self.process is None:
            return
        self.process.kill()
        self.process.terminate()
        os.killpg(self.process.pid, signal.SIGTERM)


class AppHandle(object):
    serial: str

    """获取设备id"""

    def get_devices(self) -> List[str]: ...

    def connect_device(self, serial: str) -> Feature: ...

    def disconnect_device(self, serial: str) -> Feature: ...

    """
    获取设备信息
    {'model': 'iPhone8Plus', 'name': '“陈波”的测试机', 'version': '14.2', 'cpu': 'arm64'}
    """

    def get_info(self, serial: str) -> List: ...

    """输出第三方安装包"""

    def app_list(self, serial: str) -> List[str]: ...

    """重启"""

    def reboot(self, serial: str) -> None: ...

    """截图"""

    def screenshot(self): ...

    # 安装APP
    def install(self, path: Union[str, Path]): ...

    # 卸载APP
    def uninstall(self, pkg_name: str): ...

    def switch_serial(self, serial: str) -> None:
        self.serial = serial

    def device(self, serial: str = None) -> Any: ...


class AdbHandle(AppHandle):
    """
    命令行运行操作，当前为同步命令模式
    """

    def __init__(self):
        super(AdbHandle, self).__init__()
        import adbutils
        adbutils.AdbClient()
        self.serial = ""

    def get_devices(self) -> List[str]:
        """
        获取设备的udid
        """
        return [device.serial for device in adb.device_list()]

    def check_state(self, serial: str) -> bool:
        """
        device: 设备号
        """
        return serial in self.get_devices()

    def connect_device(self, serial: str) -> Feature:
        """
        发起设备连接，一般用于远程连接
        """
        if not serial:
            return Feature.fail().set_message('设备ID不能为空！')
        if self.check_state(serial):
            return Feature.success().set_message(f"设备[{serial}]已连接！")
        try:
            messsage: str = adb.connect(serial, timeout=3.0)
        except AdbTimeout as e:
            return Feature.fail().set_message(f'设备[{serial}]连接超时。请重试！')

        if 'connected' in messsage:
            return Feature.success()
        if 'authenticate' in messsage:
            return Feature.fail().set_message(f'设备[{serial}]连接失败。请重试或检查USB授权状态后重试！')
        if 'cannot' in messsage:
            return Feature.fail().set_message(f'设备[{serial}]连接被拒绝！')
        return Feature.fail().set_message(f'未知错误:{messsage}')

    def disconnect_device(self, serial: str) -> Feature:
        """
        断开设备连接，一般用于远程连接
        Example returns:
            - "disconnected 192.168.190.101:5555"
        """
        if not self.check_state(serial):
            return Feature.success().set_message(f'[{serial}]未连接！')

        messsage: str = adb.disconnect(serial)
        if 'disconnected' in messsage:
            return Feature.success().set_message(f'[{serial}]已断开连接！')
        else:
            return Feature.fail().set_message(f'未知错误:{messsage}')

    def app_list(self, serial: str = None) -> List[str]:
        """输出第三方安装包"""

    def device(self, serial: str = None) -> AdbDevice:
        udid = ""
        if serial:
            udid = serial
        elif self.serial:
            udid = self.serial
        if not udid:
            raise RuntimeError("the serial is not found")
        return adb.device(udid)

    def install(self, path: Union[str, Path]):
        self.device().install(path)

    def uninstall(self, pkg_name: str):
        self.device().uninstall(pkg_name)

    def getlog(self, serial: str):
        """日志"""
        if self.check_state(serial):
            self.switch_serial(serial)
            print("abi", self.device().getprop("ro.product.cpu.abi"))
            print("sdk", self.device().getprop("ro.build.version.sdk"))
            stream: str = self.device().shell("logcat", stream=True)
            # logcat | grep OneLoginManager
            with stream:
                f = stream.conn.makefile()
                for _ in range(100):  # read 100 lines
                    line = f.readline()
                    print("Logcat:", line.rstrip())
                f.close()

    def get_info(self) -> List:
        """android 获取设备信息
        """
        # product = name, model, version, cpu
        name = ['name', 'model', 'version', 'cpu']
        getprop = [
            'getprop ro.product.brand',
            'getprop ro.product.model',
            'getprop ro.build.version.release',
            'getprop ro.product.cpu.abi'
        ]
        shell = ' && '.join(getprop)
        info_list = []
        for serial in self.get_devices():
            try:
                d = adb.device(serial)
                ro = d.shell(cmdargs=shell, timeout=3000).splitlines()
                info = dict(zip(name, ro))
                info["udid"] = serial
                print(info)
                info_list.append(info)
            except Exception:
                pass
        return info_list


class _xctestThread(threading.Thread):
    """
    通过访问  http://127.0.0.1:8200/status  确定 WebDriverAgent 的链接状态
    """

    def __init__(self, udid: str, port: int = 8200):
        super().__init__()
        self.udid = udid
        self.port = port

    def run(self) -> None:
        print(f'xctest: {threading.current_thread()}')
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        Device(self.udid).xctest("com.facebook.WebDriverAgentRunner.xctrunner", env={"USB_PORT": self.port})


class _relayThread(threading.Thread):

    def __init__(self, udid: str, port: int = 8200):
        super().__init__()
        self.udid = udid
        self.port = port

    def run(self) -> None:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        _relay.relay(Device(self.udid), self.port, 8100, True)


class TidHandle(AppHandle):
    """
    https://www.cnblogs.com/finer/p/14811683.html
    集成思路
    首先要提前将 WDA 安装到 iOS设备中 并在设置中信任开发者，确保WDA可以正常启动
    将 WDA 的bundle_id (Bundle Identifier) 作为 一个配置/常量，保存在 框架工程中， tidevice wdaproxy 需要
    在 通过 webdriver 启动driver 前，通过 tidevice 的 cmd 或者 自己封装实现的 wdaproxy 启动 WDA & 端口转发 ，这时候 local_port(本地端口)需要 记录
    在 通过 webdriver 启动driver 前，修改 driver 启动需要的配置
    添加 webDriverAgentUrl : "http://127.0.0.1:" + str(local_port)
    如果有设置 useNewWDA 为 True 的话，需要 改为 False
    wdaLocalPort 也可以不设置了
    使用新的配置 启动 driver ，就可以执行测试逻辑了
    所有任务执行完成后，最好主动检查&回收 tidevice 进程
    建议
    如果Mac环境 建议先保留原有的流程
    在集成后实际测试使用过程中发现，tidevice wdaproxy 方式，wda不是很稳定，偶尔会出现通信异常，重启wda的现象，具体原因还没有分析出来，如果后续多次验证其稳定后，可以再根据实际需求决定是否全都使用tidevice wdaproxy
    如果Mac环境保留原有的流程 ， 别忘记增加 是Linux/Windows 还是 Mac 环境的判断
    """

    def __init__(self):
        super(TidHandle, self).__init__()
        self.serial = ""
        self._xctest_t: threading.Thread = None
        self._iproxy_t: threading.Thread = None

    @staticmethod
    def get_devices() -> List[str]:
        """ios 获取设备id"""
        return [info.udid for info in Usbmux().device_list()]

    def start_wda(self, udid: str) -> str:
        """
        必须udid启动 WebDriverAgent
        tidevice -u 679c48afa066538330baad04892da34b5264bf55 wdaproxy -B com.facebook.WebDriverAgentRunner.ht2022.xctrunner --port 8100
        tidevice -u 00008030-000C05612110802E wdaproxy -B com.facebook.WebDriverAgentLib1638862464.xctrunner --port 8100
        wdaproxy -p 8100 -u 679c48afa066538330baad04892da34b5264bf55
        通过访问  http://127.0.0.1:8200/status  确定 WebDriverAgent 的链接状态
        """
        if udid not in self.get_devices():
            return "设备未连接！"
        self.end_wda()
        port = 8200  # 这里后期如果需要运行多台设备，请使用动态端口
        self._xctest_t = _xctestThread(udid=udid, port=port)
        # self._iproxy_t = _relayThread(udid=udid, port=port)
        self._iproxy_t = CmdThread(f"tidevice -u {udid} relay {port} 8100", 3000)
        self._xctest_t.start()
        self._iproxy_t.start()
        return f"WebDriverAgent start successful: http://127.0.0.1:{port}"

    def end_wda(self):
        if self._iproxy_t:
            self._iproxy_t = None
        if self._xctest_t:
            self._xctest_t = None

    def get_info(self, udid=None) -> list:
        """ios 获取设备信息
        {'model': 'iPhone8Plus', 'name': '“陈波”的测试机', 'version': '14.2', 'cpu': 'arm64'}
        """
        info_list = []
        if udid:
            devices = udid
        else:
            devices = self.get_devices()

        for udid in devices:
            info = Device(udid).device_info()
            try:
                model = config.iphone_model[info["ProductType"]]
            except KeyError as e:
                model = None
                logger.warning("设备[{0}]marketName[{1}]无法解析!".format(udid, info["ProductType"]))
            info_list.append({
                "udid": udid,
                "name": info["DeviceName"],
                "version": info["ProductVersion"],
                "cpu": info["CPUArchitecture"],
                "model": model
            })
        return info_list

    def reboot(self, udid: str) -> None:
        pass

    def app_list(self) -> List[str]:
        """
        查询第三方列表
        """
        instruments = self.device().connect_instruments()
        # 设备上全部App信息列表 包含 系统应用和插件，通过 Type 可以区分App
        apps = instruments.app_list()
        # 只筛选用户安装的App列表
        user_app_list = [app for app in apps if app["Type"] == "User"]
        return user_app_list

    def screenshot(self):
        """
        ios 通过tidevice 截图保存到指定目录
        """
        self.device().screenshot().conver("RGB").save(setting.app.screenshot_path)

    def device(self, serial: str = None) -> Device:
        udid = ""
        if serial:
            udid = serial
        elif self.serial:
            udid = self.serial
        if not udid:
            raise RuntimeError("the serial is not found")
        return Device(udid)

    def install(self, path: Union[str, Path]) -> int:
        """安装成功后返回"""
        try:
            logger.debug(f'开始安装[{path}]')
            bundle_id = self.device().app_install(path)
            logger.debug(f"安装包[{path}]成功:{bundle_id}")
        except tidevice.exceptions.ServiceError:
            logger.error("应用认证异常，安装失败！")
            return 0
        else:
            return 1

    def uninstall(self, pkg_name: str):
        self.device().app_uninstall(pkg_name)

    def install_wda(self):
        """com.facebook.WebDriverAgentRunner.xctrunner"""
        "CFBundleIdentifier"
        for app_info in self.app_list():
            if app_info["CFBundleIdentifier"] == "com.facebook.WebDriverAgentRunner.xctrunner":
                logger.debug("已安装: com.facebook.WebDriverAgentRunner.xctrunner")
                return 1
        if self.install(setting.app.ipa_path.__str__()):
            return 1
        else:
            return 0


tid: TidHandle = TidHandle()
add: AdbHandle = AdbHandle()

if __name__ == '__main__':
    # d = adb.device('XPL0220525009326')
    #
    # print(d.shell('getprop ro.product.name && getprop ro.build.version.release', timeout=300))
    from walnut_agent.script.util_handle import setting
    tid.switch_serial("")
    tid.install(setting.app.runner_path)
    pass
