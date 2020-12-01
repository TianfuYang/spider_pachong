import scrapy


class HttpViewSpider(scrapy.Spider):
    name = 'http_view'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://www.httpbin.org/user-agent']

    def parse(self, response):
        print(response.text)
        yield scrapy.Request(self.start_urls[0],dont_filter=True)
