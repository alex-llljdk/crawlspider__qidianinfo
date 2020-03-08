# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import  cursors

#使用conn同步处理数据
class QidianPipeline(object):
    def __init__(self):
        dbparams ={
                'host':'127.0.0.1', #IP
                'port':3306 ,  #port
                'user':'root', #user
                'password':'root', #password
                'database':'qidian_item',
                'charset':'utf8',#字符集
        }
        self.conn= pymysql.connect(**dbparams) #传入数据库信息
        self.cursor = self.conn.cursor(); #数据库游标
        self._sql = None #信息接口

    def process_item(self, item, spider):
        #传入sql信息，调用sql
        self.cursor.execute(self.sql,(item['title'],item['author'],item['status'],item['type'],item['brief'],item['contents'],item['image'],item['url']))
        #传送数据
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
        insert into qidian(id,title,author,status,type,brief,contents,image,url) values(Null,%s,%s,%s,%s,%s,%s,%s,%s)
        """
            return self._sql
        return self._sql



#使用Scrapy  Twisted 异步处理数据
class QiDianTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',  # IP
            'port': 3306,  # port
            'user': 'root',  # user
            'password': 'root',  # password
            'database': 'qidian_item',
            'charset': 'utf8',  # 字符集
            'cursorclass':cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
              self._sql = """
              insert into qidian(id,title,author,status,type,brief,contents,image,url) values(Null,%s,%s,%s,%s,%s,%s,%s,%s)
              """
              return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)

    def insert_item(self,cursor,item):
        cursor.execute(self.sql, (
        item['title'], item['author'], item['status'], item['type'], item['brief'], item['contents'], item['image'],
        item['url']))

    def handle_error(self,error,item,spider):
        print("="*10+'error'+'='*10)
        print(error)
        print("=" * 10 + 'error' + '=' * 10)