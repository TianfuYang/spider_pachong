# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    like_count = scrapy.Field()
    # origin_url = scrapy.Field()
    reader = scrapy.Field()
    subjects = scrapy.Field()
    # pub_time = scrapy.Field()