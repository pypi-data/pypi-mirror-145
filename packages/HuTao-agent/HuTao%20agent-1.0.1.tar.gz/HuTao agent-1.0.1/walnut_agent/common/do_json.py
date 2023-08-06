import datetime
import json
import os
from loguru import logger


def loads(json_str):
    """将传入的JSON串反序列化成字典
    """
    try:
        return json.loads(json_str)
    except json.decoder.JSONDecodeError:
        logger.error("JSON格式错误")


def dumps(raw_dict, isFormat=False):
    """将传入的字典序列化成JSON串
    """
    if isFormat:
        return json.dumps(raw_dict, indent=4, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    else:
        return json.dumps(raw_dict, ensure_ascii=False, cls=DateEncoder)


def load(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data
    except IOError:
        logger.error("没有找到{}，请确认！！".format(filepath))
    except json.decoder.JSONDecodeError:
        logger.error("JSON格式错误")


def store(filepath, data, isFormat=True):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(filepath, 'w', encoding="utf-8") as f:
        if isFormat:
            f.write(dumps(data, isFormat))  # 导出json正常显示中文
        else:
            f.write(json.dumps(data, ensure_ascii=False))  # 导出json正常显示中文


# list 转成Json格式数据
def listToJson(lst):
    import numpy as np
    keys = [str(x) for x in np.arange(1, len(lst) + 1)]
    dict_json = dict(zip(keys, lst))
    return dict_json


# 对json类部分内容重新改写，来处理datetime这种特殊日期格式
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    logger.debug("请确认现在正在调试")
