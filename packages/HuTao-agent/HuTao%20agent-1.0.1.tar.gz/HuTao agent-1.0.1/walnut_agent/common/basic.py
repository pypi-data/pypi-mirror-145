import logging
import unittest
from pathlib import Path

from airtest.core.android.adb import *
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.ios import iosPoco

from walnut_agent.common import config
from walnut_agent.common.Fzpagpoco import PKpoco
from walnut_agent.common.Install_yuerpage import WSSTestcase as W
from walnut_agent.script.case_class import Platform
from walnut_agent.script.util_handle import route
from walnut_agent.script.http_handle import master_service


class HTCaseError(Exception):
    pass


"""
class Platform(Enum):
    ios = 1
    android = 2
"""


class HuTao(unittest.TestCase):
    connect = None
    basename = None
    script_root = None
    platform = ''

    @classmethod
    def setUpClass(cls):
        """

        """
        if config.remote_info["platform"] == Platform.Android:
            prot = 5037
            devices = config.remote_info["devices"]
            device = f'Android://127.0.0.1:{prot}/{devices}'
            auto_setup(__file__, logdir=route.LOG_PATH, devices=[device])
            cls.poco = PKpoco(AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False))
            cls.connect = connect_device(device)
            cls.connect.start_recording()
        elif config.remote_info["platform"] == 1:
            auto_setup(__file__, logdir=config.LOG_PATH,
                       devices=["ios:///http://127.0.0.1:8100//00008030-001C49EC34BA802E"])
            cls.poco = iosPoco()

        logging.info(f'----------------初始化环境-----------------')

    def setUp(self):
        logging.info('============================用例开始执行======================')

    def tearDown(self):
        logging.info('============================脚本执行结束======================')

    @classmethod
    def tearDownClass(cls):
        if cls.connect:
            MP4_PATH: Path = route.LOG_PATH / 'output.mp4'
            cls.connect.stop_recording(MP4_PATH.__str__())
        cls.path = sys.modules[cls.__module__].__file__
        script: Path = Path(cls.path)
        tag = config.remote_info["tag"]
        zip_file: Path = route.package(route.LOG_PATH, f'{tag.tag}|{script.stem}.air.zip')
        # 上传zip包
        master_service.upload_log(zip_file)
        route.remove(zip_file)
        logging.info(f'----------------测试结果已输出-----------------')
