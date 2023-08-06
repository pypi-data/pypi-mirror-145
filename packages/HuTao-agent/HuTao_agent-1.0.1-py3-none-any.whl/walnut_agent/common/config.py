"""配置文件,用来存放各种路径"""
import os
import platform
import random
from pathlib import Path

run_platform = platform.system()
# 项目根目录
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))

# 设置的日志目录
LOG_PATH = BASE_DIR / "log"

# Airtest报表导出路径
export_path = BASE_DIR / "export"

REPORT_PATH = BASE_DIR / "report"

'''通用配置'''
report_path = LOG_PATH / 'report.html'
# print(report_path)
out_files = 'log.html'

airtest_result = LOG_PATH / '__init__.py'

'''ADNROID的配置'''
android_case_path = BASE_DIR / 'test_case_android' / 'case'

android_log_path = BASE_DIR / 'log'

android_address = ["Android://127.0.0.1:5037/192.168.137.219:5555"]

'''IOS的配置'''
IOS_case_path = BASE_DIR / 'test_case_ios' / 'case'

IOS_log_path = BASE_DIR / 'log'

IOS_address = ["ios:///http://127.0.0.1:8100//00008030-001C49EC34BA802E"]

mobile_path = os.path.dirname(__file__) + '/static/onion_android/mobile.csv'

num = random.randint(0, 8)
texts = ["anyu", "paopao", "paoc", "opao", "C44", "cc5", "cb6", "cc8", "cd9"]

platform = ['ios', 'android', 'h5']

remote_info = {}

fast_bundle_id = "com.yupaopao.runner.xctrunner"

# 数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': 'rm-bp16oswaje5z14jrb.mysql.rds.aliyuncs.com',
#         'PORT': 3306,
#         'USER': "tool_trw",
#         'PASSWORD': "DTKvgxaspqXjG96P",
#         'NAME': 'tool',  # 预先创建好的数据库名
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': "root",
        'PASSWORD': "123456",
        'NAME': 'make_data_web',  # 预先创建好的数据库名
    }
}
# 表结构
test_record_cols = ("appid", "version_name", "version_code", "begin_time", "end_time", "phone_brand", "phone_type",
                    "phone_sys", "target_time", "tester", "udid", "ANR_count", "crash_count", "tid", "bug_number",
                    "phone_name", "yppno")
run_status = {-1: "运行失败", 0: "运行中", 1: "运行成功", 2: "手动终止", 3: "重试中", 4: "重试失败", 5: "手动收集", 6: "终止失败",
              7: "上报失败"}

# 机型与内部编号转换
iphone_model = {"iPhone7,2": "iPhone 6",
                "iPhone7,1": "iPhone 6 Plus",
                "iPhone8,1": "iPhone 6s",
                "iPhone8,2": "iPhone 6s Plus",
                "iPhone8,4": "iPhone SE",
                "iPhone9,1": "iPhone 7",
                "iPhone9,3": "iPhone 7",
                "iPhone9,2": "iPhone 7 Plus",
                "iPhone9,4": "iPhone 7 Plus",
                "iPhone10,1": "iPhone 8",
                "iPhone10,4": "iPhone 8",
                "iPhone10,2": "iPhone 8 Plus",
                "iPhone10,5": "iPhone 8 Plus",
                "iPhone10,3": "iPhone X",
                "iPhone10,6": "iPhone X",
                "iPhone10,8": "iPhone XR",
                "iPhone11,2": "iPhone XS",
                "iPhone11,4": "iPhone XS Max",
                "iPhone11,6": "iPhone XS Max",
                "iPhone12,1": "iPhone 11",
                "iPhone12,3": "iPhone 11 Pro",
                "iPhone12,5": "iPhone 11 Pro Max",
                "iPhone12,8": "iPhone SE",
                "iPhone13,1": "iPhone 12 mini",
                "iPhone13,2": "iPhone 12",
                "iPhone13,3": "iPhone 12 Pro",
                "iPhone13,4": "iPhone 12 Pro Max",
                "iPhone14,4": "iPhone 13 mini",
                "iPhone14,5": "iPhone 13",
                "iPhone14,2": "iPhone 13 Pro",
                "iPhone14,3": "iPhone 13 Pro Max"}

environment = "PRO"

# 代理配置
proxies = {"http": "http://127.0.0.1:8888",
           "https": "http://127.0.0.1:8888"}


def create_a_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {3: random.randint(0, 9),
             4: [5, 7, 9][random.randint(0, 2)],
             5: [i for i in range(10) if i != 4][random.randint(0, 8)],
             7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
             8: random.randint(0, 9), }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


if __name__ == '__main__':
    print(BASE_DIR)
    # print(IOS_case_path)
    # print(android_cases_path)
    print(android_case_path)
    # print(android_log_path)
    # print(create_a_phone())
