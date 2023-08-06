# -*- coding: UTF-8 -*-
import re
from walnut_agent.common.http_request import HttpRequest
from loguru import logger
from walnut_agent.common.do_db import DataOp, dbname


def listToStr(source_list: list):
    return str(source_list).replace("'", "").replace(" ", "").lstrip("[").rstrip("]")


def collect_ios_monkey_log(record_id):
    kv = {}
    sql = "SELECT appid,tester,begin_time,version_name,phone_name,yppno FROM {0}.test_record_ios WHERE record_id={1}".format(
        dbname, record_id)
    with DataOp() as db:
        result = db.fetchOne(sql)
        # 引用次数大于1的变量单独赋值
        phone_name = result["phone_name"]
        # 运行失败、运行中、重连失败、停止失败时运行collect_reportLog，流转状态为手动收集
        if result["run_status"] not in [-1, 2, 3, 4, 6]:
            msg = "本次测试(ip:{0} record_id:{1})的运行状态不是运行失败、运行中、手动终止、重连失败、停止失败中的一种，无法手动收集日志！". \
                format(record_id, phone_name)
            logger.warning(msg)
        else:
            appid = result["appid"]
            version_name = result["version_name"]
            jira_op = JiraOp(appid, domain="mat")

            # 收集crash日志信息
            bug_infos = jira_op.collectLog(yppno=result["yppno"], begin_time=result["begin_time"],
                                          end_time=result["end_time"])
            bug_infos = jira_op.bugDistinct(bug_infos, version_name)
            report_info = jira_op.batchReport(bug_infos, version_name, result["tester"])
            if isinstance(report_info, tuple):
                kv["ANR_count"] = report_info[0]
                kv["crash_count"] = report_info[1]
                bug_numbers = report_info[2]
                if len(bug_numbers) > 0:
                    # 将列表掐头去尾转换成字符串，用于存入数据库
                    kv["bug_numbers"] = listToStr(bug_numbers)
                    msg = "收集日志完毕，本次测试（设备[{0}] record_id:{1}）提交的BUG编号如下:{2}".format(phone_name, record_id, bug_numbers)
                else:
                    msg = "收集日志完毕，本次测试（设备[{0}] record_id:{1}）发现重复或无效的log但未发现新的log".format(phone_name, record_id)
                logger.info(msg)
                run_status = 5
            else:
                msg = "设备[{0}]提交BUG失败！{1}".format(phone_name, report_info)
                run_status = 7
                logger.error(msg)
            kv["run_status"] = run_status
            db.update("test_record", kv, "record_id={0}".format(record_id))
    return msg


class JiraOp:
    def __init__(self, appid, domain="jira"):
        # SSO登录
        self.hr = HttpRequest()
        url_execution = "https://sso.yupaopao.com/login?service=http://{0}.yupaopao.com/".format(domain)
        resp = self.hr.request("GET", url_execution).text
        execution = re.findall('<input type="hidden" name="execution"\n                       value="(.*?)"/>', resp)[0]
        header = {"content-type": "application/x-www-form-urlencoded"}
        sso_body = {"username": "huzhiming", "password": "Aa578231407", "_eventId": "submit", "geolocation": None,
                    "execution": execution}
        resp = self.hr.request("post", "https://sso.yupaopao.com/login", headers=header, data=sso_body)
        # 合并两次重定向的cookies
        resp.history[0].cookies.update(resp.history[1].cookies)
        self.login_cookies = resp.history[0].cookies
        with DataOp() as db:
            self.app_info = db.fetchOne(
                "SELECT appid, assignee_ios, pkg_name, appid_mat FROM {0}.app_info WHERE appid={1};".format(
                    dbname, appid))

    def collectLog(self, yppno=None, begin_time=None, end_time=None, record_id=None) -> dict:
        import time
        bug_infos = {}
        appid_mat = self.app_info["appid_mat"]
        if record_id:
            with DataOp() as db:
                record_info = db.fetchOne("SELECT begin_time, end_time, yppno FROM {0}.test_record WHERE record_id={1}"
                                          ";".format(dbname, record_id))
                begin_time = record_info["begin_time"]
                end_time = record_info["end_time"]
                yppno = record_info["yppno"]
        elif not (yppno and begin_time and end_time):
            return "收集Crash日志时入参错误！"
        # 将时间转换为毫秒级时间戳
        startDay = int(time.mktime(time.strptime(begin_time, "%Y-%m-%d %H:%M:%S")) * 1000)
        endDay = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")) * 1000)
        param = "particle=DAY&startDay={0}&endDay={1}&type=crash&idType=userId&appId={2}&platform=ios&userId={3}&articleNumber=2000". \
            format(startDay, endDay, appid_mat, yppno)
        crash_infos = self.hr.request("GET", "https://mat.yupaopao.com/userLog/list?{0}".format(param)).json()["result"]
        for crash_info in crash_infos:
            crash_reason = crash_info["reason"]
            param = "particle=DAY&startDay={0}&endDay={1}&type=crash&idType=userId&userId={2}&appId={3}&platform=ios&reason={4}&articleNumber=2000".format(
                startDay, endDay, yppno, appid_mat, crash_reason)
            # 同一crash reason下，获取到一个uuid之后即可退出
            uuid = self.hr.request("GET", "https://mat.yupaopao.com/userLog/detail?{0}".format(param)).json()["result"][
                "result"][0]["uuid"]
            param = "startDay={0}&endDay={1}&uuid={2}".format(startDay, endDay, uuid)
            bug_infos[crash_reason] = \
            self.hr.request("GET", "https://mat.yupaopao.com/crashlog/detailById?{0}".format(param)).json()["result"][
                "originLog"]
        return bug_infos

    def createVersion(self, version_name):
        data = {"name": version_name, "project": "CRAS", "expand": "operations"}
        resp = self.hr.request("POST", "http://jira.yupaopao.com/rest/api/2/version", cookies=self.login_cookies,
                               json=data).text
        return resp

    # 根据生成的log提交bug
    def batchReport(self, distinct_info: dict, version_name: str, tester: str):
        ANR_count = 0
        crash_count = 0
        bug_number = []
        # 提交bug之前检测登录是否成功
        if type(self.login_cookies) == str:
            return self.login_cookies
        for bug_title in distinct_info.keys():
            # 拼接bug描述，并提交bug
            assignee = self.app_info["assignee_ios"]
            report_info = self.bugReport(bug_title, distinct_info[bug_title], version_name, tester, assignee,
                                         issuetype="测试BUG-IOS")
            try:
                bug_number.append(re.findall('"key":"(.+?)"', report_info)[0])
            except IndexError:
                if report_info.find("指定的的报告人不是用户") != -1:
                    msg = "提交BUG失败，请检查测试人名称！"
                elif report_info.find("不存在") != -1:
                    msg = "提交BUG失败，经办人{0}不存在，请检查经办人配置！".format(assignee)
                else:
                    msg = report_info
                logger.warning(msg)
                return msg
            else:
                crash_count += 1
        return ANR_count, crash_count, bug_number

    # 提交BUG
    def bugReport(self, summary, description, versions, reporter, assignee, components="BUG", project_key="CRAS",
                  priority="P0", issuetype="测试BUG-Android"):
        # jira限制summary长度
        if len(summary) >= 255:
            summary = summary[:255]
        jira_body = {"fields": {"summary": summary, "issuetype": {"name": issuetype}, "project": {"key": project_key},
                                "description": description, "assignee": {"name": assignee},
                                "priority": {"name": priority},
                                "components": [{"name": components}], "versions": [{"name": versions}],
                                "reporter": {"name": reporter}}}
        resp = self.hr.request("POST", "http://jira.yupaopao.com/rest/api/2/issue/", json=jira_body,
                               cookies=self.login_cookies).text
        # 版本号不存在时，自动创建版本后再次提交BUG
        if resp.find('"版本名 “{0}”无效"'.format(versions)) != -1:
            self.createVersion(versions)
            resp = self.hr.request("POST", "http://jira.yupaopao.com/rest/api/2/issue/", json=jira_body,
                                   cookies=self.login_cookies).text
        return resp

    def bugDistinct(self, bug_infos: dict, version_name):
        bug_titles = bug_infos.keys()
        # 通过BUG标题、影响版本和项目进行bug去重
        url = "http://jira.yupaopao.com/rest/api/2/search/?jql=project%20%3D%20CRAS%20AND%20affectedVersion%20%3D%20" \
              "{0}".format(version_name)
        resp = self.hr.request("GET", url, cookies=self.login_cookies).text
        jira_bug_titles = re.findall("\"summary\":\"(.+?)\"", resp)
        num = len(bug_titles)
        # 查询目标版本下的bug标题并去重
        for i in range(num):
            bug_title = bug_titles[i]
            if bug_title in jira_bug_titles:
                bug_infos.pop(bug_title)
        return bug_infos


if __name__ == '__main__':
    JiraOp(1, "mat").collectLog(111791024, "2022-03-02 00:00:00", "2022-03-03 16:00:00")
