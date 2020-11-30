import scrapy
from qsbk.qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider' # 定义爬虫的名字
    allowed_domains = ['baidu.com']  # 指定域名 这就不是该域名下的链接就不会去爬取了
    start_urls = ['https://www.baidu.com/']  # 开始的url
    # 网站访问后返回的数据会自动传给下面的parse方法
    def parse(self, response):
        print('res',type(response))
        content = response.xpath('//p[@class="lh"]')
        print('conta',content)
        for i in content:
            auto = i.xpath('.//a/text()').get()
            print('suto',auto)
            # con = {"name":auto}
            item = QsbkItem(name=auto)
            yield item