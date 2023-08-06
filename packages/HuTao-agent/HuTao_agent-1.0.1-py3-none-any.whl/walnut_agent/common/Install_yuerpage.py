# -*- encoding=utf8 -*-
__author__ = "paomian"

# from tools.out_log import Logger
import os

from airtest.core.api import *
# from test_case_android import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class WSSTestcase():
    """下包，切环境"""

    def __init__(self):
        auto_setup(__file__)
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

        # auto_setup(__file__, logdir=android_log_path + '/' + os.path.basename(__file__), devices=android_address)

    # 安装鱼耳直播app测试包---小米手机调试版本
    def test_installpage(self):
        print("=====================》》》》》》》》》》》》》》》》》检测安装包未安装，开始下包安装-----操作即将开始")
        # 确保程序重新启动
        start_app("com.yupaopao.mcd")
        stop_app("com.yupaopao.mcd")
        start_app("com.yupaopao.mcd")
        poco = self.poco
        poco(text="鱼耳直播").click()
        # poco(text="所有").click()
        poco(text="6.5.0").click()
        poco(text="5.4.0").click()
        # 点击第一个包
        # w,h=device().get_current_resolution()
        # touch([0.5*w,0.5*h])
        # 点击第一个测试包
        poco(text="测试")[0].click()
        poco(text="安装").click()
        time.sleep(60)
        # 下滑，拉出下载页
        poco.swipe([0.5, 0.03], [0.5, 0.8], duration=0.2)
        while True:
            if poco(text="下载完成").exists():
                poco(text="下载完成").click()
                break
            else:
                time.sleep(10)
        time.sleep(1)
        poco("com.miui.packageinstaller:id/left_button_msg").click()
        time.sleep(1)
        poco("com.miui.packageinstaller:id/install_btn").click()
        # 安装中
        while True:
            if poco("com.miui.packageinstaller:id/start_button").exists():
                poco("com.miui.packageinstaller:id/start_button").click()
                break
            else:
                time.sleep(10)

        # 上滑，回到首页
        poco.swipe([0.5, 0.99], [0.5, 0.7], duration=0.2)

    # 下载包后，切环境步骤，自动切到测试环境

    # def test_environment_test(self):
    #     poco = self.poco
    #     poco("com.yangle.xiaoyuzhou:id/tvAgree").click()
    #     log("测试内容", "这是标题one")
    #     # 等青少年模式弹框加载
    #     time.sleep(4)
    #     # 判断青少年弹窗，没有点击我的
    #     if poco(text="知道了").exists():
    #         poco(text="知道了").click()
    #         # 地址授权
    #         WST = WSSTestcase()
    #         WST.test_mi_authorization()
    #         # 线上消除广告弹窗
    #         poco.swipe([0.03, 0.5], [0.8, 0.5], duration=0.2)
    #         poco(text="我的").click()
    #     else:
    #         # 地址授权
    #         WST = WSSTestcase()
    #         WST.test_mi_authorization()
    #         # 线上消除广告弹窗
    #         poco.swipe([0.03, 0.5], [0.8, 0.5], duration=0.2)
    #         poco(text="我的").click()

    def test_environment_test(self):
        poco = self.poco


        # 切换环境,点击环境按钮
        poco("com.yangle.xiaoyuzhou:id/debug_tag").click()
        time.sleep(1)
        poco(text="release").click()
        time.sleep(1)
        poco("com.yangle.xiaoyuzhou:id/debug_switch_btn_dev").click()
        time.sleep(2)
        # poco.swipe([0.03, 0.5], [0.8, 0.5], duration=0.2)
        # time.sleep(2)
        # 隐私政策点击同意
        # poco("com.yangle.xiaoyuzhou:id/tvAgree").click()
        # 上滑，回到首页
        # poco.swipe([0.5, 0.99], [0.5, 0.7], duration=0.2)
        # simple_report(__file__, logpath=True, logfile="logss.txt", output="log1.html")

    # 小米手机授权

    def test_mi_authorization(self):
        poco = self.poco
        if poco(text="仅在使用中允许").exists():
            poco(text="仅在使用中允许").click()
        else:
            pass

    def test_connect_iphone(self):
        # os.system('adb connect 192.168.137.96:5555')
        os.system('adb devices')

    # def test_api_installpage(self):
    #     print("=====================》》》》》》》》》》》》》》》》》检测安装包未安装，开始下包安装-----操作即将开始")
    #     poco = self.poco
    #     r = requests.get(
    #         f'https://hulk.yupaopao.com/media/MCD_Android/xxq/5.5.0/55020211012-165832_9058/xxq_5.5.0_9058_20211012-165832_Inner_Arm32_ypp.apk'
    #     )
    #     time.sleep(20)
    #
    #     install("https://hulk.yupaopao.com/media/MCD_Android/xxq/5.5.0/55020211012-165832_9058/xxq_5.5.0_9058_20211012-165832_Inner_Arm32_ypp.apk")
    #
    #     # poco(text="5.4.0").click()
    #     # 点击第一个包


if __name__ == '__main__':
    S = WSSTestcase()
    print("xxxxxxxxxxxxxxxxxxxxxx")
    S.test_environment_test()
