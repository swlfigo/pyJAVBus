# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql
import requests
from scrapy.exceptions import DropItem


class JavbusPipeline(object):

    def __init__(self):
        pass


    @classmethod
    def from_settings(cls, settings):
        print("Spider Singleton!")
        return cls()  # 相当于conn付给了这个类，self中可以得到

    def open_spider(self, spider):
        print('open pipelines')
        javDBName = 'JavBusPython'
        DBHost = "localhost"
        DBPort = 3306
        DBUser = 'root'
        DBPassWord = '22f25f9d81f4d21d'
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

        self.dbConn.commit()
        # self.downloadImagesWithItem(item = item)


    def _handle_error(self, failure, item, spider):
        print(failure)



