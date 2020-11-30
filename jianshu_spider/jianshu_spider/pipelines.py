# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

'''同步存储'''
# class JianshuSpiderPipeline:
#     def __init__(self):
#         dbparams = {
#             'host': '127.0.0.1',
#             'port': 3306,
#             'user': 'root',
#             'password': 'password',
#             'database': 'jianshu',
#             'charset': 'utf8'
#         }
#         self.conn = pymysql.connect(**dbparams)
#         self.cursor = self.conn.cursor()
#         self._sql = None
#
#     def process_item(self, item, spider):
#         self.cursor.execute(self.sql, (item['title'], item['content'], item['url']))
#         self.conn.commit()
#         print('*-*'*20,'已添加++++++')
#         return item
#
#     @property
#     def sql(self):
#         print('*-*' * 20, '进来了++++++')
#         if not self._sql:
#             self._sql = """
#             insert into article(id,title,content,url) values (null,%s,%s,%s)
#             """
#             return self._sql
#         return self._sql

'''异步存储'''


class jianshuTwistedPipeline():
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        print('*-*' * 20, '进来了++++++')
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,url,reader,like_count,subjects) values (null,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
        item['title'], item['content'], item['url'], item['reader'], item['like_count'], item['subjects']))
        # self.conn.commit()

    def handle_error(self, error, item, spider):
        print('=^=' * 5, 'error_start:')
        print(error)
        print('=^=' * 5, 'error_end')
