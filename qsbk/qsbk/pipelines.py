# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class QsbkPipeline:
    def __init__(self):
        self.fp = open('baidudu.json','w',encoding='utf-8')
    def open_spider(self,spider):
        print('爬虫begin')
    def process_item(self, item, spider):
        # with open('baidu.json','a',encoding='utf-8') as f:
        #     json.dump(item,f,ensure_ascii=False)
        #     f.write('\n')
        item_json=json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(item_json+'\n')
        return item
    def close_spider(self,spider):
        self.fp.close()
        print('爬虫over')