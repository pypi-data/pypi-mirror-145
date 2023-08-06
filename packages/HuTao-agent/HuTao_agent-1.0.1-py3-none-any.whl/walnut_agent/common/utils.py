import io
import json
import re
from loguru import logger
from datetime import datetime
import subprocess


def split(_s: str) -> list:
    """分割字符串
    """
    return re.split(',|，|;|\||；|_', _s)


def save_json_file(dict_str: dict, json_file: str) -> 'None':
    """保存json文件
    """
    logger.info("开始写入json文件: {}".format(json_file))

    with io.open(json_file, 'w', encoding="utf-8") as outfile:
        my_json_str = json.dumps(dict_str, ensure_ascii=False, indent=4)
        if isinstance(my_json_str, bytes):
            my_json_str = my_json_str.decode("utf-8")

        outfile.write(my_json_str)

    logger.info("写入json文件成功！")


def load_json_file(json_file: str) -> dict:
    """加载json文件
    """
    with io.open(json_file, "r+", encoding="utf-8") as f:
        try:
            return json.loads(f.read())
        except (KeyError, TypeError, FileNotFoundError):
            msg = "json文件读取失败，请检查文件路径: {}".format(json_file)
            logger.error(msg)


def tid(name: str):
    return ''.join([name, '-', datetime.today().strftime('%Y%m%d%H%M%S')])


def match_version(user_agent: str):
    # activity = ''
    version = ''
    match = re.search("com|pc(.+?);", user_agent)
    if match:
        # activity_match = re.search("com\.[a-z]*\.[a-z]*", match.group())
        # if activity_match:
        #     activity = activity_match.group()
        version_match = re.search("\d+\.?\d+\.?\d+\.?\d?", match.group())
        if version_match:
            version = version_match.group()
    return version


def json_dumps(obj, **kwargs):
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, **kwargs)


def json_loads(s, **kwargs):
    if not isinstance(s, str):
        return s
    return json.loads(s)


def switch(value, func=int):
    """
    数据类型转换，转换是吧返回空
    switch([1], tuple)  -->  (1,)
    switch("12")        -->  12
    """
    try:
        return func(value)
    except ValueError as e:
        logger.error("%s -> 转换失败 %s" % (e.args[0], str(value)))
        return None
    except TypeError as e:
        logger.error("%s -> 转换失败 %s" % (e.args[0], str(value)))
        return None


if __name__ == '__main__':
    pass
