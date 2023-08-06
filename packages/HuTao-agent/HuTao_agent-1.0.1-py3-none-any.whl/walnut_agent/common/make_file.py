import os
import time
import shutil
from loguru import logger

from walnut_agent.common import config


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        logger.info("创建目录成功: %s" % path)

    else:
        logger.info("目录已存在，不需要创建: %s" % path)


def make_file():
    mkdir(config.LOG_PATH)
    mkdir(config.airtest_result)


def get_task_path(job_id: int):
    """
    获取 task 当前存在的目录
    """
    root = config.REPORT_PATH
    t = time.localtime()
    task_path = root / str(job_id) / time.strftime("%Y-%m-%d-%H-%M-%S", t)
    mkdir(task_path)
    return task_path


def clear_log():
    """
    清空log文件夹下所有文件
    """
    if os.path.exists(config.LOG_PATH):
        shutil.rmtree(config.LOG_PATH)
    mkdir(config.LOG_PATH)
    logger.info("日志目录已清空: %s" % config.LOG_PATH)


if __name__ == '__main__':
    clear_log()
