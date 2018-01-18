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
                    print('存在 %s 封面 %s' % (str(item['code']), cover_name))
                    self.logger.syLog('存在 %s 封面 %s' % (str(item['code']), cover_name))
                    break
                try:
                    ir = requests.get(coverURL, timeout=2)
                except Exception as e:
                    self.logger.syLog('下载 %s 封面 %s 错误 Error : %s ' % (str(item['code']), cover_name, str(e)))
                    print('下载 %s 封面 %s 错误 Error : %s ' % (str(item['code']), cover_name, str(e)))
                    break
                if ir.status_code == 200:
                    with open(coverPath, 'wb') as f:
                        f.write(ir.content)
                        f.close()
                        self.logger.syLog('下载 %s 封面 %s 成功' % (str(item['code']), cover_name))
                        print('下载 %s 封面 %s 成功' % (str(item['code']), cover_name))


            #样例图片下载
            elif item['type'] == 'samplePic':
                list_name = url.split('/')
                # 图片名称
                file_name = str(list_name[len(list_name) - 1])
                filePath = os.path.join(rootPath, file_name)
                # 存在图片则不用下载
                if self.fileOperator.isExistsFilePath(filePath) == True:
                    self.logger.syLog('存在 %s 样品图 %s' % (str(item['code']), file_name))
                    print('存在 %s 样品图 %s' % (str(item['code']), file_name))
                    break
                try:
                    ir = requests.get(url, timeout=2)
                except Exception as e:
                    self.logger.syLog('下载 %s 样品图 %s 错误 Error : %s ' % (str(item['code']), file_name, str(e)))
                    print('下载 %s 样品图 %s 错误 Error : %s ' % (str(item['code']), file_name, str(e)))
                    break
                if ir.status_code == 200:
                    with open(filePath, 'wb') as f:
                        f.write(ir.content)
                        f.close()
                        self.logger.syLog('下载 %s 样品图 %s 成功' % (str(item['code']), file_name))
                        print('下载 %s 样品图 %s 成功' % (str(item['code']), file_name))