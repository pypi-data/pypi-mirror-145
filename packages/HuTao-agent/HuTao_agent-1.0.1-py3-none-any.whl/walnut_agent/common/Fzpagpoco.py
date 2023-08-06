#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
封装 Appium WebDriver, 提供安全查找元素方法
'''

__author__ = 'paomian'

import logging

from airtest.core.api import *


class PKpoco(object):
    @property
    def platform(self):
        return self.Spoco.desired_capabilities['platformName']

    def __init__(self, spoco):
        self.Spoco = spoco

    def is_element_text_exists(self, text):
        """
        UI text元素是否存在
        """
        return self.Spoco(text=text).exists()

    def is_element_name_exists(self, name):
        """
        UI name元素是否存在
        """
        return self.Spoco(name=name).exists()

    def find_element_by_Name(self, name):
        """
        根据 name 查找 UI 元素
        """
        logging.warning(f'正在识别元素: [{name}] ')
        try:
            if self.is_element_name_exists(name) == True:
                return self.Spoco(name=name)

        except:
            logging.warning(f'UI元素不存在: [{name}] ')
            print("识别失败，找不到目标元素:", name)
            snapshot(msg="失败截图")
            return self

    def find_element_by_Text(self, text):
        """
            Text查找元素
        """
        logging.warning(f'正在识别元素: [{text}] ')
        try:
            if self.is_element_text_exists(text) == True:
                # print(self.Spoco(text=text))
                # print(poco.is_element_exists(text))
                return self.Spoco(text=text)
        except:
            logging.warning(f'Text匹配失败: [{text}] ')
            print("识别失败，找不到目标元素:", text)
            snapshot(filename="test.png", msg="失败截图")
            return self

    def find_Text(self, text):
        logging.warning(f'正在识别元素: [{text}] ')
        return self.Spoco(text=text)

    def find_name(self, name):
        logging.warning(f'正在识别元素: [{name}] ')
        return self.Spoco(name=name)

    def find_desc(self, desc):
        logging.warning(f'正在识别元素: [{desc}] ')
        return self.Spoco(desc=desc)

    def find_all(self):
        # logging.warning(f'正在识别元素: [{text}] ')
        return self

    def up(self):
        '''
        上滑
        '''
        xy = self.Spoco.get_screen_size()
        print(xy)
        x = xy[0]
        y = xy[1]
        swipe([x * 0.5, y * 0.9], [x * 0.5, y * 0.1])

    def down(self):
        '''
        下滑
        '''
        xy = self.Spoco.get_screen_size()
        print(xy)
        x = xy[0]
        y = xy[1]
        swipe([x * 0.5, y * 0.1], [x * 0.5, y * 0.9])

    def left(self):
        '''
        左滑
        '''
        xy = self.Spoco.get_screen_size()
        print(xy)
        x = xy[0]
        y = xy[1]
        swipe([x * 0.9, y * 0.5], [x * 0.1, y * 0.5])

    def right(self):
        '''
        右滑
        '''
        xy = self.Spoco.get_screen_size()
        print(xy)
        x = xy[0]
        y = xy[1]
        swipe([x * 0.1, y * 0.5], [x * 0.9, y * 0.5])

    def back(self):
        '''
        智能手机返回
        '''
        xy = self.Spoco.get_screen_size()
        print(xy)
        x = xy[0]
        y = xy[1]
        swipe([x * 0.03, y * 0.5], [x * 0.9, y * 0.5])

    def click(self):
        pass

    def set_text(self, name):
        pass

    def shouquan(self):
        """
        手机权限授权框
        """
        # 红米手机权限图片授权弹框
        if PKpoco.is_element_text_exists(self, "仅在使用该应用时允许"):
            PKpoco.find_element_by_Text(self, "仅在使用该应用时允许").click()
        # 三星s20 图片授权弹框
        elif PKpoco.is_element_text_exists(self, "允许"):
            PKpoco.find_element_by_Text(self, "允许").click()
        else:
            pass

