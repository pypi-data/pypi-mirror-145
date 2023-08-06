#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
枚举类
"""

__author__ = 'chenbo'

from enum import Enum, IntEnum, unique

from fast_dict import dictionary
from typing import Optional, Any, TypeVar, Generic

T = TypeVar('T')


@unique
class Platform(Enum):
    ios = 1
    Android = 2

    @classmethod
    def match(cls, index, default: 'Platform' = None) -> Optional['Platform']:
        try:
            return Platform(int(index))
        except Exception:
            return default


"""testcase的运行状态
"""


class Status(Enum):
    INIT = 0
    RINGING = 1
    ERROR = 2

    @classmethod
    def match(cls, index, default: 'Status' = None) -> Optional['Status']:
        try:
            return Status(int(index))
        except Exception:
            return default


"""task的运行状态
"""


class TaskStatus(Enum):
    INIT = 1
    ONLOAD = 2
    RUNNING = 3
    FINISH = 4
    UNUSUAL = 5

    @classmethod
    def match(cls, index, default: 'TaskStatus' = None) -> Optional['TaskStatus']:
        try:
            return Status(int(index))
        except Exception:
            return default


"""
这是一个带状态的存储对象
state: bool 状态, true or false
msg: str 信息提示, 默认 ''
data: Any 数据, 默认 None
"""


class Feature(Generic[T]):

    def __init__(self, state: bool):
        self._state: bool = state
        self._msg: str = ''
        self._func: Any = None
        self._data: T = None

    @staticmethod
    def success() -> 'Feature':
        return Feature(True)

    @staticmethod
    def fail() -> 'Feature':
        return Feature(True)

    @property
    def state(self) -> bool:
        return self._state

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def data(self) -> T:
        return self._data

    def set_message(self, value: str) -> 'Feature':
        self._msg = value
        return self

    def set_func(self, func: Any, arg: dict = None) -> 'Feature':
        self._func = (func, arg)
        return self

    def exec(self) -> Any:
        """
        执行函数，如果状态为 false 或者 function 为空, 则不执行，返回 msg 提示
        """
        if self._state and self._func:
            return exec(*self._func)
        else:
            return self._msg

    def set_data(self, value: T) -> 'Feature':
        self._data = value
        return self

    def is_fail(self) -> bool:
        return False if self._state else True

    def is_success(self) -> bool:
        return not self.is_fail()


if __name__ == '__main__':
    fs = Feature[str].success().set_message('执行成功')
    print(fs.data)
    print(fs.msg)
