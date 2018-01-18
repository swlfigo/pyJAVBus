# -*- coding:utf-8 -*-

import pymysql
from javbus.Utils import syLogger
import re

# 单例模式
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# 数据库记录类
@singleton
class dbManager():
    javDBName = 'JavBusPython'
    DBHost = "localhost"
    DBPort = 3306
    DBUser = 'root'
    DBPassWord = '22f25f9d81f4d21d'
    DBCharset = 'utf8'


    def __init__(self):
        self.logger = syLogger.syLoggerManager()


    def __executeStrings(self,sqlCommandsList,cursor):
        if len(sqlCommandsList) == 0 or cursor is None:
            return
        try:
            for sql in sqlCommandsList:
                cursor.execute(sql)
        except Exception as e:
            self.logger.syLog(str(e))

    # 执行多sql语句
    def executeSQLArray(self, sqlStringArray):
        if len(sqlStringArray) == 0:
            print ('SQLString数据为空')
            return
        conn = pymysql.connect(self.DBHost, self.DBUser, self.DBPassWord, self.javDBName,
                               charset=self.DBCharset)
        cursor = conn.cursor()
        try:
            for sql in sqlStringArray:
                cursor.execute(sql)
                print('sql执行成功')
        except Exception as e:
            self.logger.syLog(str(e))
        finally:
            cursor.close()
            conn.commit()
            conn.close()


    # 执行命令
    def execute(self, executeString):
        fetchResult = []
        conn = pymysql.connect(self.DBHost,self.DBUser,self.DBPassWord,self.javDBName,charset=self.DBCharset)
        cursor = conn.cursor()
        try:
            results = cursor.execute(executeString)
            fetchResult = cursor.fetchall();
            print('sql执行成功')
            # print('executeString:%s'%executeString)
        except Exception as e:
            self.logger.syLog(str(e))
        cursor.close()
        conn.commit()
        conn.close()
        # self.dbLock.release()
        return fetchResult




    # 执行命令(字典返回)
    def executeWithDictReturn(self, executeString):
        fetchResult = []
        conn = pymysql.connect(self.DBHost,self.DBUser,self.DBPassWord,self.javDBName,charset=self.DBCharset)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            results = cursor.execute(executeString)
            fetchResult = cursor.fetchall();
            print('sql字典执行成功')
        except Exception as e:
            self.logger.syLog(str(e))

        cursor.close()
        conn.commit()
        conn.close()
        return fetchResult

