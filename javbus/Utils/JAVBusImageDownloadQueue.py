# -*- coding:utf-8 -*-
import queue
import threading
import requests
from javbus.Utils import syLogger
from javbus.Utils import syFileOperator
import os

class javBusImageDownloadQueue(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.downloadLock = threading.Lock()
        self.fileOperator = syFileOperator.syFileOperator()
        self.logger = syLogger.syLoggerManager()
        # 资源目录
        self.sourcePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.fileOperator.currentPath))),'PYJAVBUS')
        self.logInfo = []


    def run(self):
        while True:
            item = self.queue.get()
            rootPath = item['code']
            rootPath = os.path.join(self.sourcePath, rootPath)
            if self.fileOperator.isExistsFilePath(rootPath) == False:
                self.fileOperator.createDirPath(rootPath)
            url = item['url']

            #封面图
            if item['type'] == 'cover':
                coverURL = url
                coverSplit = coverURL.split('/')
                cover_name = str(coverSplit[len(coverSplit) - 1])
                coverPath = os.path.join(rootPath, cover_name)
                if self.fileOperator.isExistsFilePath(coverPath) == True:
                    info = '存在 %s 封面 %s ' % (str(item['code']), cover_name)
                    print(info)
                    self.logInfo.append(info)
                else:
                    try:
                        ir = requests.get(coverURL, timeout=2)
                    except Exception as e:
                        info = '下载 %s 封面 %s 错误 Error : %s ' % (str(item['code']), cover_name, str(e))
                        print(info)
                        self.logInfo.append(info)
                        self.queue.task_done()
                    if ir.status_code == 200:
                        with open(coverPath, 'wb') as f:
                            f.write(ir.content)
                            f.close()
                            info = '下载 %s 封面 %s 成功' % (str(item['code']), cover_name)
                            self.logInfo.append(info)
                            print('===>写入 %s 封面 %s 成功' % (str(item['code']), cover_name))
                            print('CoverPath:%s'%str(coverPath))
                    self.queue.task_done()



            #样例图片下载
            elif item['type'] == 'samplePic':
                list_name = url.split('/')
                # 图片名称
                file_name = str(list_name[len(list_name) - 1])
                filePath = os.path.join(rootPath, file_name)
                # 存在图片则不用下载
                if self.fileOperator.isExistsFilePath(filePath) == True:
                    info = '存在 %s 样品图 %s' % (str(item['code']), file_name)
                    self.logInfo.append(info)
                    print(info)
                else:
                    try:
                        ir = requests.get(url, timeout=2)
                    except Exception as e:
                        info = '下载 %s 样品图 %s 错误 Error : %s ' % (str(item['code']), file_name, str(e))
                        print(info)
                        self.logInfo.append(info)
                        self.queue.task_done()
                    if ir.status_code == 200:
                        with open(filePath, 'wb') as f:
                            f.write(ir.content)
                            f.close()
                            info = '下载 %s 样品图 %s 成功' % (str(item['code']), file_name)
                            self.logInfo.append(info)
                            print('下载 %s 样品图 %s 成功' % (str(item['code']), file_name))
                            print('===>写入 %s 样品图 %s 成功' % (str(item['code']), file_name))
                            print('CoverPath:%s' % str(filePath))
                    self.queue.task_done()


    def _stop(self):
        self.logger.syLogManyLines(self.logInfo)
        print('End Queue')
