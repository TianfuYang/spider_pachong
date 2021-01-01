# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class newFangSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    areas = scrapy.Field()
    state = scrapy.Field()
    style = scrapy.Field()
    address = scrapy.Field()
    ori_url = scrapy.Field()