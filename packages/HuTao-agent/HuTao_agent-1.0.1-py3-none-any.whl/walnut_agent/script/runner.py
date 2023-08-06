# -*- coding: utf-8 -*-

# @File    : runner.py
# @Date    : 2022-01-19
# @Author  : chenbo

"""
编译外部的*.py 文件，并加入到 unittest 中运行
"""
import time
import traceback
import unittest
from pathlib import Path
from threading import Thread
from typing import Union, Any, List

from airtest.core.api import auto_setup, connect_device
from loguru import logger

from walnut_agent.script.case_class import Feature, Platform
from walnut_agent.script.http_handle import master_service
from walnut_agent.script.util_handle import route
from walnut_agent.unit.report import TestRunner


def load_script(file_path: Union[str, Path]) -> Feature:
    file_path = Path(file_path)
    if not file_path.exists():
        return Feature.fail().set_message(f'脚本文件不存在:{file_path}')

    with file_path.open('r', encoding='utf8') as f:
        script = f.read()

    func = compile(script.encode("utf-8"), file_path.__str__(), "exec")
    arg = {}
    arg['__file__'] = file_path.__str__()

    return Feature.success().set_func(func, arg)


def exec_script(file_path: Union[str, Path]) -> Any:
    try:
        res = load_script(file_path).exec()
    except Exception as err:
        tb = traceback.format_exc()
        logger.error("Final Error", tb)


class AirTest(unittest.TestCase):
    """
    tag: 上报日志和报表所需标记
    """
    platform: Platform = Platform.Android

    def __init__(self, script: str, tag: str, platform: Platform = None, devices: List[str] = None):
        super().__init__()
        if platform:
            self.platform = platform
        self.devices = devices if devices else []
        self.script = script
        self.tag = tag
        self.connect = None

    def setUp(self):
        self.auto_setup()
        logger.info('============================用例开始执行======================')
        self.record_screen()

    def tearDown(self):
        logger.info('============================脚本执行结束======================')
        self.report()

    def auto_setup(self):
        logger.info('============================初始化环境======================')
        route.clear_log()
        device = ""
        if self.platform == Platform.Android:
            prot = 5037
            device = f'Android://127.0.0.1:{prot}/{self.devices[0]}'
            # 安卓链接ADB，用例保存视频的
            # self.connect = connect_device(device)
        if self.platform == Platform.ios:
            prot = 8200
            device = f'iOS:///http://127.0.0.1:{prot}'

        if device:
            auto_setup(logdir=route.LOG_PATH, devices=[device])

    def report(self):
        # 结束录屏
        # if self.connect:
        #     MP4_PATH: Path = route.LOG_PATH / 'output.mp4'
        #     self.connect.stop_recording(MP4_PATH.__str__())
        #     logger.info('============================结束录屏======================')
        # else:
        #     logger.info('============================录屏失败======================')
        # 上报log 日志
        # 打包日志文件夹
        script: Path = Path(self.script)
        zip_file: Path = route.package(route.LOG_PATH, f'{self.tag}|{script.stem}.air.zip')
        # 上传zip包
        master_service.upload_log(zip_file)
        route.remove(zip_file)

        logger.info('============================日志上报成功======================')

    def runTest(self):
        script: Path = Path(self.script)
        if script.suffix == '.air':
            script = script / f'{script.stem}.py'

        exec_script(script)

    def record_screen(self):
        if self.connect:
            self.connect.start_recording()
            logger.info('=============================开始录屏=======================')


class Runner(Thread):
    """
    tag: 上报日志和报表所需标记
    """
    devices: List[str] = []
    script: List[Union[str, Path]] = []
    platform: Platform = None
    isCheck: bool = False

    def __init__(self, task_id: str, filename: str = 'report.html', version: str = "2.0.0"):
        """
        platform: 设备类型 Android / ios
        task_id: 任务id 必传
        """
        super().__init__()
        t = time.localtime()
        self.tag = f'{task_id}|{time.strftime("%Y-%m-%d-%H-%M-%S", t)}'
        self.filename = filename
        self.task_id = task_id
        self.report_name = f'{self.tag}|{filename}'
        self.version = version

    def exec(self) -> None:
        # 设置任务为运行开始状态
        master_service.task_running(self.task_id, self.tag)

        self.isCheck = True

        # 获取任务信息
        task = master_service.task_get(self.task_id)
        self.platform = task['platform']

        if not self.platform:
            logger.error("运行平台类型不正确！")
            self.isCheck = False

        # 处理设备id, 并准备设备
        self.devices: str = task['devices'].split("|")

        steps = []
        # 下载脚本文件
        try:
            self.script: List[Path] = self._get_task_info(task)
        except Exception as e:
            logger.exception("文件下载异常！")
            self.isCheck = False

        # 准备脚本
        if len(self.script) == 0:
            logger.error("没有可以运行的脚本！")
            self.isCheck = False

        if self.isCheck:
            if self.version == "1.0.0":
                suite = self._test_loader()
            else:
                suite = self._built_up()

            start_timestamp = time.time()
            runner = TestRunner(suite,
                                filename=self.report_name,
                                report_dir=route.REPORT_PATH.__str__(),
                                title='app 自动化测试报表',
                                templates=1,
                                tester='chenbo'
                                )
            result = runner.run()
            # result = unittest.TextTestRunner(verbosity=0).run(suite)
            execute_time_ms = round((time.time() - start_timestamp) * 1000, 2)

            report_file = route.REPORT_PATH / self.report_name
            # 上传报表
            master_service.upload_log(report_file)

            # 发送邮件
            # runner.send_email(host="smtp.exmail.qq.com",
            #                   port=465,
            #                   user="musen_nmb@qq.com",
            #                   password="algmmzptupjccbab",
            #                   to_addrs="3247119728@qq.com")

            # 发送钉钉通知
            url = "https://oapi.dingtalk.com/robot/send?access_token=d47928279ed45f4be919b3f927ac00cfab7ece4fbcf22c109b76bc4d77f6c1ee"
            # 发送钉钉通知
            runner.dingtalk_notice(url=url, key='执行通知:执行完成',
                                   secret='SEC8ae2c87f7c244f30523c489ab39ad34c41f45f6593f21ee3a504420f31584955',
                                   atMobiles=[17621501358],
                                   except_info=True
                                   )

        # 设置任务为运行完成状态
        master_service.task_finish(self.task_id, self.report_name.replace("|", "/"), self.tag)

    def _built_up(self) -> unittest.TestSuite:
        suite = unittest.TestSuite()

        for s in self.script:
            logger.debug('添加测试')
            suite.addTest(AirTest(script=s, platform=self.platform, devices=self.devices, tag=self.tag))

        return suite

    def _test_loader(self) -> unittest.TestSuite:
        """1.0.0版本，使用unittest.TestLoader()加载Python文件"""
        from walnut_agent.common.config import remote_info
        remote_info["tag"] = self.tag
        remote_info["devices"] = self.devices
        remote_info["platform"] = self.platform
        suite = unittest.TestSuite()
        for s in self.script:
            logger.debug('添加测试')
            suite.addTest(unittest.TestLoader().discover(start_dir=s, pattern=s.parents[0]))

        return suite

    def run(self) -> None:
        self.exec()

    # 获取steps内的脚本文件，下载到客户端本地，并解压，返回脚本本地路径
    def _get_task_info(self, task: dict) -> List[Path]:
        steps = task["steps"]
        task_root: Path = route.SCRIPT_PATH / str(task['id'])
        route.mkdir(task_root)
        script_list: List[Path] = []
        for step in steps:
            zip_name: str = step['case_path'] + '.zip'
            zip_path = task_root / zip_name
            master_service.download(step["case_dir"], zip_path)
            route.unpack(zip_path)
            script_list.append(zip_path.parents[0] / zip_path.stem)
        return script_list
