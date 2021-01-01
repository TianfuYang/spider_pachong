import scrapy
import re
from ..items import newFangSpiderItem

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
                    # yield scrapy.Request(url=esf_url, meta={'info': (province, city_name)},
                    #                      callback=self.esf_parse)
                    break
                break


    def newhouse_parse(self, response):
        province, city = response.meta.get("info")
        print('返回', province, city)
        newhouse_list = response.xpath(".//div[@class='nhouse_list']//li[not(@style)]")
        for newhouse in newhouse_list:
            # print('循环了',newhouse)
            detail = newhouse.xpath(".//div[@class='nlc_details']")
            name = detail.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            ori_url = response.urljoin(detail.xpath(".//div[@class='nlcd_name']/a/@href").get())
            price_long = ''.join(detail.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub("\s","",price_long)
            areas_long = ''.join(detail.xpath(".//div[contains(@class,'house_type')]//text()").getall())
            areas_long2 = re.sub("\s","",areas_long)
            style,areas = areas_long2.split("－") if "－" in areas_long2 else ('暂无','暂无')
            state =newhouse.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            address = detail.xpath(".//div[@class='address']/a/@title").get()

            print('名字是：', name,ori_url,'价格：',price,"面积",areas,"样式",style,"地址",address)
            item = newFangSpiderItem(province=province,city=city,name=name,ori_url=ori_url,price=price,
                                     areas=areas,style=style,state=state,address=address)
            yield item
        if response.xpath(".//div[@class='page']//a[last()]/@href").get() == "尾页":
            next_url = response.xpath(".//div[@class='page']//a[last()-1]/@href").get()
            if next_url:
                print('下一页是：',next_url)
                print('第%s页结束了' % response.xpath(".//div[@class='page']//a[@class='active']/text()").get())
                yield scrapy.Request(url=response.urljoin(next_url),callback=self.newhouse_parse,meta={
                    'info':(province,city)
                })
        else:
            print("{}，{}新房爬取完毕".format(province,city))




    # def esf_parse(self,response):
    #     province, city = response.meta.get("info")
    #     print('返回', province, city)

