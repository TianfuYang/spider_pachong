import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from ..items import JianshuSpiderItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/[p]/[a-z0-9]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        print('new返回', type(response))
        title = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        content = ''.join(response.xpath("//article[@class='_2rhmJa']//p/text()").getall())
        url = response.url
        read = ','.join(response.xpath("//div[@class='s-dsoj']//span/text()").getall())
        like_count = response.xpath("//span[@class='_1LOh_5']/text()").get()
        subjects = ','.join(response.xpath("//div[@class='_2Nttfz']/text()").getall())
        print(title, url, '\n', content)
        print('*' * 20)
        print('**********', read, like_count)
        # item = JianshuSpiderItem(
        #     title=title,
        #     reader=read,
        #     like_count=like_count,
        #     content=content,
        #     url=url,
        #     subjects=subjects
        # )
        # yield item
