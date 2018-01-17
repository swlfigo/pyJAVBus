# -*- coding:utf-8 -*-
import os
import shutil

#文件类型黑名单
#不需要统计文件类型
fileTypeBlackList = ['.git' , '.idea' , '.DS_Store' ]


class syFileOperator():
    def __init__(self):
        #获取当前文件所在的文件夹
        self.currentPath = os.getcwd()


    #判断文件路径是否存在文件
    def isExistsFilePath(self, filePath):
        if os.path.exists(filePath) == False:
            return False
        else:
            return True


    #移除文件夹
    def removeDirPath(self,dirPath):
        if self.isExistsFilePath(dirPath):
            shutil.rmtree(dirPath)

    #移除文件
    def removeFilePath(self,filePath):
        if self.isExistsFilePath(filePath):
            os.remove(filePath)

    #创建一个新的文件夹
    def createDirPath(self,dirPath):
        if self.isExistsFilePath(dirPath):
            print ('存在文件夹')
        else:
            os.mkdir(dirPath)

    #复制文件夹到文件夹
    def copyFileWithDir(self,oriPath,desPathDir):
        if oriPath is None or desPathDir is None:
            return
        if self.isExistsFilePath(oriPath) == False:
            return
        if self.isExistsFilePath(desPathDir) == False:
            self.createDirPath(desPathDir)


        shutil.copy(oriPath, desPathDir)


    #获取单文件的大小Size（单位 M）
    def getFileSize(self,filePath):
        if self.isExistsFilePath(filePath) == False:
            return 0
        else:
            size = os.path.getsize(filePath)
            return (size/1024/1024)

    #获取文件夹总文件大小
    #返回元组 (文件总大小,文件数量)
    def getDirSize(self,dirPath):
        filesize = 0
        fileCount = 0
        if self.isExistsFilePath(dirPath) == False:
            return (0,0)
        else:

            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for parent , dirnames , filenames in os.walk(dirPath):

                # 文件信息
                for filename in filenames:
                    currentPath = os.path.join(parent, filename)
                    #排除文件夹
                    if (os.path.isdir(currentPath)) == False:
                        #获取多少M
                        if len(fileTypeBlackList) > 0 :
                            for type in fileTypeBlackList:
                                if currentPath in type:
                                    continue
                                else:
                                    filesize += os.path.getsize(currentPath) / 1024 / 1024
                                    fileCount += 1
                        else:
                            filesize += os.path.getsize(currentPath) / 1024 / 1024
                            fileCount += 1

        return (filesize , fileCount)
