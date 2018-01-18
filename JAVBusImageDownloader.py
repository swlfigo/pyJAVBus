# -*- coding:utf-8 -*-

import requests
import os
import queue
import sys
from javbus.Utils import syFileOperator
from javbus.Utils import syLogger
from javbus.Utils import JAVBusMySQLDBManager
from javbus.Utils import JAVBusImageDownloadQueue



class JAVImageDownloader():


    def __init__(self):

        self.fileOperator = syFileOperator.syFileOperator()
        self.dbManager = JAVBusMySQLDBManager.dbManager()
        self.logger = syLogger.syLoggerManager()
        # 创建资源目录
        #  PYJAVBUS ...  (项目文件根)javbus (同级) /javbus / Utils / currentPath
        self.sourcePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.fileOperator.currentPath))),'PYJAVBUS')
        if self.fileOperator.isExistsFilePath(self.sourcePath) == False:
            self.fileOperator.createDirPath(self.sourcePath)
        #Queue
        self.downloadImageQueue = queue.Queue()
        #Resource
        self.downloadSource = []


    def startDownLoadImage(self):
        print('SourceDownloadPath:%s'%self.sourcePath)
        sqlString = '''SELECT * FROM %s'''%self.dbManager.javTableName
        items = self.dbManager.executeWithDictReturn(sqlString)
        if len(sqlString) == 0 or sqlString is None:
            self.logger.syLog('无下载资源')
            return

        for item in items:
            if len(item['samplePic']) == 0 or item['samplePic'] is None or len(item['cover']) == 0:
                self.logger.syLog('无样例图片')
                continue
            rootPath = item['code']
            rootPath = os.path.join(self.sourcePath, rootPath)
            if self.fileOperator.isExistsFilePath(rootPath) == False:
                self.fileOperator.createDirPath(rootPath)
            # 样品图
            samplePic = item['samplePic']
            #如果没有图片则不用添加
            if samplePic is not None and len(samplePic) > 0:
                samplePicArray = samplePic.split('||')
                for picURLAddress in samplePicArray:
                    downInfoDict = {

                        "url":str(picURLAddress),
                        "code":str(item['code']),
                        "type":"samplePic"

                    }
                    self.downloadSource.append(downInfoDict)

            if item['cover'] is not None :
                downInfoDict = {

                    "url":str(item['cover']),
                    "code":str(item['code']),
                    "type":"cover"

                }
                self.downloadSource.append(downInfoDict)

        #多线程下载
        for i in range(10):
            queue = JAVBusImageDownloadQueue.javBusImageDownloadQueue(self.downloadImageQueue)
            queue.setDaemon(True)
            queue.start()
        for i in range(len(self.downloadSource)):
            self.downloadImageQueue.put(self.downloadSource[i])
            if i == len(self.downloadSource) - 1 :
                self.downloadImageQueue.put(None)

        self.downloadImageQueue.join()





if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    imageDownloader = JAVImageDownloader()
    imageDownloader.startDownLoadImage()
