# -*- coding:utf-8 -*-
import requests
import os
import sys
from javbus.Utils import syFileOperator
from javbus.Utils import syLogger
from javbus.Utils import JAVBusMySQLDBManager



class JAVImageDownloader():


    def __init__(self):
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))
        self.fileOperator = syFileOperator.syFileOperator()
        self.dbManager = JAVBusMySQLDBManager.dbManager()
        self.logger = syLogger.syLoggerManager()
        # 创建资源目录
        #  PYJAVBUS ...  (项目文件根)javbus (同级) /javbus / Utils / currentPath
        self.sourcePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.fileOperator.currentPath))),
                                       'PYJAVBUS')
        if self.fileOperator.isExistsFilePath(self.sourcePath) == False:
            self.fileOperator.createDirPath(self.sourcePath)

    def startDownLoadImage(self):
        print('SourceDownloadPath:%s'%self.sourcePath)
        sqlString = '''SELECT * FROM %s'''%self.dbManager.javDBName
        items = self.dbManager.executeWithDictReturn(sqlString)
        if len(sqlString) == 0 or sqlString is None:
            self.logger.syLog('无下载资源图片')
        for item in items:
            if len(item['samplePic']) == 0 or item['samplePic'] is None or len(item['cover']) == 0:
                self.logger.syLog('无样例图片')
                continue
            rootPath = item['code']
            rootPath = os.path.join(self.sourcePath, rootPath)
            if self.fileOperator.isExistsFilePath(rootPath) == False:
                self.fileOperator.createDirPath(rootPath)
            samplePic = item['samplePic']
            samplePicArray = samplePic.split('||')
            #样品图
            for picURLAddress in samplePicArray:
                list_name = picURLAddress.split('/')
                # 图片名称
                file_name = str(list_name[len(list_name) - 1])
                filePath = os.path.join(rootPath, file_name)
                #存在图片则不用下载
                if self.fileOperator.isExistsFilePath(filePath) == True:
                    self.logger.syLog('存在 %s 样品图 %s'%(str(item['code']) , file_name))
                    continue
                try:
                    ir = requests.get(picURLAddress, timeout=2)
                except Exception as e:
                    self.logger.syLog('下载 %s 样品图 %s 错误 Error : %s '%(str(item['code']) , file_name , str(e)))
                    continue
                if ir.status_code == 200:
                    with open(filePath, 'wb') as f:
                        f.write(ir.content)
                        f.close()
                        self.logger.syLog('下载 %s 样品图 %s 成功' % (str(item['code']), file_name))

            #封面图
            coverURL = item['cover']
            coverSplit = coverURL.split('/')
            cover_name = str(coverSplit[len(coverSplit) - 1])
            coverPath = os.path.join(rootPath, cover_name)
            if self.fileOperator.isExistsFilePath(coverPath) == True:
                self.logger.syLog('存在 %s 封面 %s' % (str(item['code']), cover_name))
                continue
            try:
                ir = requests.get(coverURL, timeout=2)
            except Exception as e:
                self.logger.syLog('下载 %s 封面 %s 错误 Error : %s ' % (str(item['code']), cover_name, str(e)))
                return
            if ir.status_code == 200:
                with open(coverPath, 'wb') as f:
                    f.write(ir.content)
                    f.close()
                    self.logger.syLog('下载 %s 封面 %s' % (str(item['code']), cover_name))


if __name__ == '__main__':
    imageDownloader = JAVImageDownloader()
    imageDownloader.startDownLoadImage()
