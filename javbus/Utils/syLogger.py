# -*- coding:utf-8 -*-
import os
import datetime


#单例模式
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


#log记录类
@singleton
class syLoggerManager():

    isDebugMode = True

    def __init__(self):

        print ('Logger Init -----> if console shows many times , there is a bug check!')

        # self.logFilePath = os.getcwd()
        self.logFilePath = os.path.dirname(os.path.realpath(__file__))
        self.logFilePath = os.path.join(self.logFilePath , 'log.txt')
        if os.path.exists(self.logFilePath):
            #存在log文件
            #py3.0
            # f = open(self.logFilePath,'a',encoding='utf8')
            #py2.0
            f = open(self.logFilePath, 'a')
            f.write('\n\n今天日志' + '==============' +str(datetime.date.today()) + '==============')
        else:
            f = open(self.logFilePath,'w')
            f.write('今天日志' + '==============' +str(datetime.date.today()) + '==============')
            f.close()


    def syLog(self,info):
        if info is None:
            return
        if self.isDebugMode == True:
            f = open(self.logFilePath,'a')
            f.write('\n %s =====>  %s'%(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) , info))
            f.close()

    def syLogManyLines(self,infoArray):
        if infoArray is None:
            return
        if self.isDebugMode == True:
            f = open(self.logFilePath, 'a')
            for info in infoArray:

                f.write('\n %s' % (info))
            f.close()