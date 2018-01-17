# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql
import requests
from scrapy.exceptions import DropItem
from javbus.Utils import syFileOperator

class JavbusPipeline(object):

    def __init__(self):

        self.fileOperator = syFileOperator.syFileOperator()
        #创建资源目录
        self.sourcePath = os.path.join(os.path.dirname(self.fileOperator.currentPath),'PYJAVBUS')
        if self.fileOperator.isExistsFilePath(self.sourcePath) == False:
            self.fileOperator.createDirPath(self.sourcePath)

    @classmethod
    def from_settings(cls, settings):
        print("Spider Singleton!")
        # javDBName = 'JavBusPython'
        # DBHost = "127.0.0.1"
        # DBPort = 3306
        # DBUser = 'root'
        # DBPassWord = 'ad953268'
        # DBCharset = 'utf8'
        # conn = pymysql.connect(DBHost, DBUser, DBPassWord, javDBName, charset=DBCharset)
        # # conn = pymysql.connect(host = DBHost, user = DBUser, passwd = DBPassWord , port = DBPort ,charset=DBCharset)
        # cursor = conn.cursor()
        # # cursor.execute('''CREATE DATABASE IF NOT EXISTS JavBusPython''')
        # cursor.execute('''CREATE TABLE IF NOT EXISTS javBusTable(
        #                     id          INTEGER           PRIMARY KEY     auto_increment,
        #                     title        TEXT,
        #                     cover      TEXT,
        #                     code       TEXT,
        #                     date   TEXT,
        #                     duration  TEXT,
        #                     series TEXT,
        #                     type TEXT,
        #                     actress TEXT,
        #                     magnet TEXT,
        #                     size TEXT,
        #                     samplePic TEXT,
        #                     link TEXT,
        #                     LastIndexFlag TEXT
        #                     )''')
        # cursor.execute("set names 'utf8'")
        return cls()  # 相当于conn付给了这个类，self中可以得到

    def open_spider(self, spider):
        print('open pipelines')
        javDBName = 'JavBusPython'
        DBHost = "127.0.0.1"
        DBPort = 3306
        DBUser = 'root'
        DBPassWord = 'ad953268'
        DBCharset = 'utf8'
        self.dbConn = pymysql.connect(DBHost, DBUser, DBPassWord, javDBName, charset=DBCharset)
        # conn = pymysql.connect(host = DBHost, user = DBUser, passwd = DBPassWord , port = DBPort ,charset=DBCharset)
        self.cursor = self.dbConn.cursor()
        # cursor.execute('''CREATE DATABASE IF NOT EXISTS JavBusPython''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS javBusTable(
                                    id          INTEGER           PRIMARY KEY     auto_increment,
                                    title        TEXT,
                                    cover      TEXT,
                                    code       TEXT,
                                    date   TEXT,
                                    duration  TEXT,
                                    series TEXT,
                                    type TEXT,
                                    actress TEXT,
                                    magnet TEXT,
                                    size TEXT,
                                    samplePic TEXT,
                                    link TEXT,
                                    LastIndexFlag TEXT
                                    )''')
        self.cursor.execute("set names 'utf8'")


    def close_spider(self, spider):
        self.dbConn.commit()
        self.cursor.close()
        self.dbConn.close()
        print("Spider Done!")


    def process_item(self, item, spider):

        self.updateOrInsertItem(item,spider)

        return item

    def updateOrInsertItem(self,item,spider):
        if item['code'] is None or item['code'] =='' :
            raise DropItem("Missing Content ")
            return

        sqlString = ''' SELECT * FROM javBusTable where code = '%s' ''' % item['code']
        self.cursor.execute(sqlString)
        res = self.cursor.fetchall()

        title = item['title']
        cover = item['cover']
        code = item['code']
        date = item['date']
        duration = item['duration']
        series = item['series']
        type = item['type']
        actress = item['actress']
        magnet = item['magnet']
        size = item['size']
        samplePic = item['samplePic']
        link = item['link']

        if len(res) == 0:
            #插入状态
            print('insert')
            sqlInsertString = "INSERT INTO javBusTable (title,cover,code,date,duration,series,type,actress,magnet,size,samplePic,link,LastIndexFlag) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (title, cover, code, date, duration, series, type, actress, magnet, size, samplePic, link, "")
            try:
                self.cursor.execute(sqlInsertString.encode('utf8'))
            except Exception as e:
                print(e)
                self.dbConn.rollBack()


        else:
            #更新状态
            print('update')
            sqlUpdateString = '''update javBusTable set title = '%s' , cover = '%s' , date = '%s' , duration = '%s' , series = '%s' , type = '%s' , actress = '%s' , magnet = '%s' , size = '%s' , samplePic = '%s' , link = '%s' WHERE code = '%s' ''' %(title,cover,date,duration,series,type,actress,magnet,size,samplePic,link,code)
            try:
                self.cursor.execute(sqlUpdateString.encode('utf8'))
            except Exception as e:
                print(e)
                self.dbConn.rollBack()
        self.downloadImagesWithItem(item = item)


    def _handle_error(self, failure, item, spider):
        print(failure)


    #下载图片
    def downloadImagesWithItem(self,item):
        if len(item['samplePic']) == 0 or item['samplePic'] is None:
            return
        rootPath = item['code']
        rootPath = os.path.join(self.sourcePath,rootPath)
        if self.fileOperator.isExistsFilePath(rootPath) == False:
            self.fileOperator.createDirPath(rootPath)
        samplePic = item['samplePic']
        samplePicArray = samplePic.split('||')
        for picURLAddress in samplePicArray:
            list_name = picURLAddress.split('/')
            # 图片名称
            file_name = str(list_name[len(list_name) - 1])
            filePath = os.path.join(rootPath,file_name)
            try:
                ir = requests.get(picURLAddress , timeout = 2)
            except Exception as e:
                print(e)
                continue
            if ir.status_code == 200:
                if self.fileOperator.isExistsFilePath(filePath) == True:
                    continue
                with open(filePath,'wb') as f:
                    f.write(ir.content)
                    f.close()



