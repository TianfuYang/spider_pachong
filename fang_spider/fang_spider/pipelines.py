# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from twisted.enterprise import adbapi
from pymysql import cursors

class newFangSpiderPipeline:
    x = 0
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'fangtianxia',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        self.x += 1
        print('*-*' * 10, '第{}条数据进来了++++++'.format(self.x))
        if not self._sql:
            self._sql = """
            insert into newhouse(id,name ,province,city,price,areas,state ,style, address,ori_url) values
             (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
        item['name'], item['province'], item['city'], item['price'], item['areas'], item['state'],
        item['style'],item['address'],item['ori_url']))
        # self.conn.commit()

    def handle_error(self, error, item, spider):
        print('=^=' * 5, 'error_start:')
        print(error)
        print('=^=' * 5, 'error_end')
