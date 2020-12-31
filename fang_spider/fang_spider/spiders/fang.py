import scrapy
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        # Cookie2 = response.headers.getlist('Set-Cookie')  # 响应
        # print(Cookie2)
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td")
            province_td = tds[1].xpath(".//text()").get()
            province_text = re.sub(r'\s', '', province_td)
            if province_text and province_text != '其它':
                province = province_text
            if province_text != '其它':
                city_tda = tds[2].xpath(".//a")
                for city in city_tda:
                    city_name = city.xpath("./text()").get()
                    city_url = city.xpath("./@href").get()
                    if city_name == '北京':
                        newhouse_url = "https://newhouse.fang.com/house/s/"
                        esf_url = "https://esf.fang.com"
                    else:
                        newhouse_url = city_url.replace("fang.com", "newhouse.fang.com/house/s/")
                        esf_url = city_url.replace("fang.com", "esf.fang.com")
                    print(province, city_name, city_url, newhouse_url, esf_url)
                    yield scrapy.Request(url=newhouse_url, meta={'info': (province, city_name)},
                                         callback=self.newhouse_parse)

    def newhouse_parse(self, response):
        province, city = response.meta.get("info")
        print('返回', province, city)
