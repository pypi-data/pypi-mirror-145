# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import decimal

import pymysql
from walnut_agent.common.config import DATABASES
from loguru import logger
# 数据库连接
username = DATABASES["default"]["USER"]
passwd = DATABASES["default"]["PASSWORD"]
hostname = DATABASES["default"]["HOST"]
dbname = DATABASES["default"]["NAME"]


class DataOp:
    def __init__(self, host=hostname, user=username, password=passwd, port=3306, dbname=dbname, returnDict=True):
        self.host = host  # 数据库主机地址
        self.port = port  # 端口号
        self.user = user  # 数据库用户名
        self.password = password  # 数据库密码
        self.returnDict = returnDict  # 是否返回字典，FALSE则返回元祖
        self.dbname = dbname  # 数据库名称

    def __enter__(self):
        # 建立连接
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
        # 建立查询
        if self.returnDict:
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)  # 指定每行数据以字典的形式返回
        else:
            self.cursor = self.conn.cursor()  # 指定每行数据以元祖的形式返回
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def fetchOne(self, sql):
        logger.debug(sql)
        # 执行SQL
        self.cursor.execute(sql)
        # 获取结果
        result = self.cursor.fetchone()  # 返回元祖/字典 （）
        logger.debug(result)
        if result is None:
            logger.debug("没有查到符合条件的记录!")
            return 0
        return result  # 返回结果

    def fetchAll(self, sql):
        logger.debug(sql)
        # 执行SQL
        self.cursor.execute(sql)
        # 获取结果
        results = self.cursor.fetchall()  # 返回列表 [(),()]
        logger.debug(results)
        if len(results) == 0:
            logger.debug("没有查到符合条件的记录!")
            return 0
        return self.resultsFormat(results)

    def otherOp(self, sql):
        try:
            # 执行SQL
            logger.debug(sql)
            self.cursor.execute(sql)
            # 查看修改行数
            affected_rows = self.conn.affected_rows()
            logger.debug("修改成功,影响行数:{}".format(affected_rows))
            # 提交到数据库执行
            self.conn.commit()
            return affected_rows
        except pymysql.DatabaseError as e:
            # 回滚
            self.conn.rollback()
            raise e

    def insert(self, tablename, cols: tuple, values: tuple):
        values_str = ''
        for value in values:
            if type(value) == int:
                values_str += "{0},".format(value)
            else:
                values_str += "'{0}',".format(value)
        # 去除末尾逗号
        values_str = values_str[:-1]
        sql = "INSERT INTO {0}.{1}{2} VALUES({3});".format(self.dbname, tablename, str(cols).replace("'", ""),
                                                           values_str)
        self.otherOp(sql)

    def delete(self, tablename, where):
        sql = "DELETE FROM {0}.{1} WHERE {2};".format(self.dbname, tablename, where)
        self.otherOp(sql)

    def update(self, tablename, kv: dict, condition):
        s = ""
        # 拼接set字符串
        for key in kv:
            if type(kv[key]) == int:
                c = "{0}={1},".format(key, kv[key])
            else:
                c = "{0}='{1}',".format(key, kv[key])
            s += c
        # 去除末尾的逗号
        s = s[:-1]
        sql = "UPDATE {0}.{1} SET {2} WHERE {3};".format(self.dbname, tablename, s, condition)
        self.otherOp(sql)

    @staticmethod
    def resultsFormat(results: list):
        for result in results:
            for key in result.keys():
                if type(result[key]) == decimal.Decimal:
                    result[key] = int(result[key])
        return results


if __name__ == '__main__':
    logger.debug("请确认现在正在调试")
