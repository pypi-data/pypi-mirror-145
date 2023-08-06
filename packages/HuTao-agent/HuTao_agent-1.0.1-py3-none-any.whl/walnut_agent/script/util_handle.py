#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取配置，设置工作路径，设置报表路径，设置日志路径
并对路径进行操作等
"""

__author__ = 'chenbo'

import shutil
import time
import zipfile
from pathlib import Path
import os
from typing import Union
import configparser
import attr
import socket
import platform

from loguru import logger


def _get_os_platform() -> str:
    """获取系统类型
    Darwin: macOs
    Windows: Windows
    Linux: Linux
    """
    return platform.system()


def _get_host_ip() -> (str, str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.0.0.1', 8080))
        ip = s.getsockname()[0]
        name = socket.gethostname()
    finally:
        s.close()
    return ip, name


localIP, hostName = _get_host_ip()
PROJECT_ROOT: Path = Path(os.path.dirname(__file__)).parents[0]


class Route(object):
    # 项目根目录
    if _get_os_platform() == "Windows":
        BASE_DIR: Path = Path(os.environ['USERPROFILE']) / 'ht_agent'
    else:
        BASE_DIR: Path = Path(os.environ['HOME']) / 'ht_agent'

    def __init__(self, root: str = None) -> None:
        if root:
            self.BASE_DIR = root
        self.__trim__()

    def __trim__(self) -> None:
        """
        整理项目路径
        """
        Route.mkdir(self.BASE_DIR)
        # 设置脚本存放目录
        self.SCRIPT_PATH = self.BASE_DIR / 'script'
        Route.mkdir(self.SCRIPT_PATH)
        # 设置的日志目录
        self.LOG_PATH: Path = self.BASE_DIR / "log"
        Route.mkdir(self.LOG_PATH)
        # Airtest报表导出路径
        self.EXPORT_PATH: Path = self.BASE_DIR / "export"
        Route.mkdir(self.EXPORT_PATH)
        # unittest 自定义报表路径
        self.REPORT_PATH: Path = self.BASE_DIR / "report"
        Route.mkdir(self.REPORT_PATH)

    def set_root(self, root: str) -> None:
        """
        重新设置项目路径
        """
        if root and isinstance(root, str):
            self.BASE_DIR = root
            self.__trim__()

    def task_route(self, job_id: str):
        t = time.localtime()
        task_path = self.REPORT_PATH / str(job_id) / time.strftime("%Y-%m-%d-%H-%M-%S", t)
        Route.mkdir(task_path)
        return task_path

    def clear_log(self):
        """
        清空log文件夹下所有文件
        """
        if self.LOG_PATH.exists():
            shutil.rmtree(self.LOG_PATH)
        Route.mkdir(self.LOG_PATH)
        logger.info("日志目录已清空: %s" % self.LOG_PATH)

    @staticmethod
    def mkdir(path: Union[str, Path]) -> None:
        """
        创建文件夹，判断是否存在，存在则不需要创建
        """
        # 转为path对象
        path = Path(path)
        if path.exists():
            return None
        os.makedirs(path)
        logger.info(f"创建目录: {path}")

    def unpack(self, zip_path: Path) -> None:
        """解压zip"""
        zip_file = zipfile.ZipFile(zip_path.__str__())
        parent: Path = zip_path.parents[0]
        name = zip_path.stem

        for names in zip_file.namelist():
            zip_file.extract(names, parent)
        zip_file.close()
        # 开始移除zip文件
        os.remove(zip_path)
        # 如果有__MACOSX,则删除__MACOSX
        macosx = parent / '__MACOSX'
        if macosx.exists():
            shutil.rmtree(macosx)

    def package(self, file_path: Path, file_name: str) -> Path:
        """
        打包成zip包
        """
        parent: Path = file_path.parents[0]
        file_name = file_name if file_name.endswith('.zip') else file_name + '.zip'
        zip_file: Path = parent / file_name

        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zip:
            for file in file_path.iterdir():
                r_name = str(file).replace(str(file_path), '')
                zip.write(file, r_name)

        return zip_file

    def remove(self, path: Union[Path, str]) -> None:
        """
        删除文件
        """
        f_path = Path(path)
        if f_path.is_file():
            os.remove(f_path)
        if f_path.is_dir():
            shutil.rmtree(f_path)


"""
项目的路径对象,实际应用中使用这个
"""
route: Route = Route()


# 读取配置文件，并转话为dictionary
class _conf:

    def __init__(self):
        file: Path = route.BASE_DIR / 'config.ini'
        logger.info(f'开始读取配置文件:{file}')
        config = configparser.ConfigParser()
        config.read(file.__str__())
        self._options = {}
        for section in config.sections():
            self._options[section] = {k: v for k, v in config.items(section)}

    def get_section(self, section: str) -> dict:
        return self._options.setdefault(section, {})


# 读取后的配置文件
conf: _conf = _conf()
# 读取后的APP节点下的配置
app_conf: dict = conf.get_section('app')
air_conf: dict = conf.get_section('airtest')

"""
项目的配置信息,实际应用中使用这个
"""


@attr.s
class setting:
    class app:
        bundle_id: str = app_conf.setdefault('bundle_id', 'com.facebook.WebDriverAgentRunner.ht2022.xctrunner')
        port: str = app_conf.setdefault('port', "8100")
        screenshot_path: Path = route.BASE_DIR / app_conf.setdefault('screenshot_path', "screenshot")
        http_host = app_conf.setdefault('http_host', 'http://192.168.25.242:18000')
        ws_host = app_conf.setdefault('ws_host', 'ws://192.168.25.242:18000')
        ipa_path: Path = PROJECT_ROOT / 'static' / 'lib' / 'wda-bixin.ipa'
        runner_path: Path = PROJECT_ROOT / 'static' / 'lib' / 'bixin-runner.ipa'

    class airTest:
        test: str = air_conf.setdefault('test', 'test')

    class agent:
        ip: str = localIP
        port: str = '10086'
        name: str = hostName


if __name__ == '__main__':
    print(_get_os_platform())
