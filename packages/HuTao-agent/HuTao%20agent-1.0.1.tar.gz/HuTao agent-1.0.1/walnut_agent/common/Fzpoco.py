#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
封装 airtest poco, 提供安全查找元素方法
'''

__author__ = 'paomian'

import logging
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# from appium import webdriver
# from appium.webdriver.webelement import WebElement
# from selenium.webdriver.support.wait import WebDriverWait


class Fzpoco(object):
    # @property
    # def platform(self):
    #     return self.drvier.desired_capabilities['platformName']

    def __init__(self, AndroidUiautomationPoco):
        self.poco = AndroidUiautomationPoco

    def is_element_exists(self, name='', predicate=None):
        """
        UI 元素是否存在
        """
        if predicate == None:
            try:
                logging.info('元素是否存在: [%s]', name)
                # self.drvier.find_element_by_id(name)
                self.poco(name=name).exists()
                return True
            except:
                logging.warning('UI元素不存在: [%s]', name)
                return False
        else:
            try:
                logging.info('元素是否匹配: [%s]', predicate)
                self.drvier.find_element_by_ios_predicate(predicate)
                return True
            except:
                logging.warning('UI元素不存在: [%s]', predicate)
                return False
    # ---------------------------------------------------------------
    def find_element_by_name(self, name):
        """
        根据 name 查找 UI 元素
        """
        try:
            # self.drvier.implicitly_wait(5)
            logging.info('正在查找元素: [%s]', name)
            return self.poco(name=name)
        except:
            logging.warning('UI元素不存在: [%s]', id)
            return self

    def find_elements_by_text(self, text):
        try:
            # self.drvier.implicitly_wait(5)
            logging.info('正在批量查找元素: [%s]', text)
            return self.poco(text=text)
        except:
            print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            logging.warning('UI元素不存在: [%s]', text)
            return self
    # ----------------------------------------------------------------------------------
    # def find_element_by_ios_predicate(self, value) -> WebElement:
    #     """
    #     iOS 谓词查找元素
    #     """
    #     try:
    #         self.drvier.implicitly_wait(5)
    #         logging.info('正在匹配谓词: [%s]', value)
    #         return self.drvier.find_element_by_ios_predicate(value)
    #     except:
    #         logging.warning('谓词匹配失败: [%s]', value)
    #         return self

    # def waitUntil(self, timeout: int, method):
    #     try:
    #         WebDriverWait(self.drvier,
    #                       timeout).until(lambda driver: method(self))
    #     except:
    #         logging.warning(f'{method}: 已等待 {timeout}s ')
    #
    # def tap_blank(self,
    #               positions: List[Tuple[int, int]] = [(0, 100)],
    #               duration: Optional[int] = None):
    #     """
    #     点击空白处
    #     """
    #     self.drvier.tap(positions=positions, duration=duration)
    #
    # def quit(self):
    #     logging.warning('session 结束\n=========================')
    #     self.drvier.quit()
    #
    # def real_driver(self):
    #     return self.drvier

    # Element 方法和属性
    @property
    def text(self):
        return ''

    def click(self):
        pass

    def send_keys(self, id):
        pass


if __name__ == '__main__':
    # print(config.desired_caps_ios)
    # poco = webdriver.Remote('http://localhost:4723/wd/hub',
    #                           config.desired_caps_ios)
    # driver = SafeDriver(driver)
    # driver.find_element_by_ios_predicate('abc')
    auto_setup(__file__, logdir=os.getcwd() + '\log')
    poco = Fzpoco(AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False))
    start_app("com.yangle.xiaoyuzhou")
    poco.find_elements_by_text("我的").click()