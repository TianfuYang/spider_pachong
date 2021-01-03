import scrapy
import re, json
from ..items import newFangSpiderItem
from ..middlewares import re_cookies


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
                    # yield scrapy.Request(url=newhouse_url, meta={'info': (province, city_name)},
                    #                      callback=self.newhouse_parse)

                    # cooki = {"cookie":"""global_cookie=dwi8uf9ky7lfteoil0w77ugjl28kjfxu44j; city=www; global_wapandm_cookie=4qqfzddnve98p4xdoo2qvct4c16kjg3r1sd; g_sourcepage=esf_fy%5Elb_pc; unique_cookie=U_n0b9vm5xw7xixtvj67lbe96cl20kjhf0ndm*2; __utma=147393320.1550169561.1609605973.1609612191.1609695300.3; __utmc=147393320; __utmz=147393320.1609695300.3.3.utmcsr=fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1609695300
                    #         """}
                    yield scrapy.Request(url=esf_url, meta={'info': (province, city_name)},
                                         callback=self.esf_parse)
                    # yield scrapy.Request(url=esf_url, headers=cooki,meta={'info': (province, city_name)},
                    #                      callback=self.esf_parse,dont_filter=True)
                    break
                break

    def newhouse_parse(self, response):
        province, city = response.meta.get("info")
        print('new返回', province, city)
        print('new返回', province, city, type(response))
        newhouse_list = response.xpath(".//div[@class='nhouse_list']//li[not(@style)]")
        for newhouse in newhouse_list:
            # print('循环了',newhouse)
            detail = newhouse.xpath(".//div[@class='nlc_details']")
            name = detail.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            ori_url = response.urljoin(detail.xpath(".//div[@class='nlcd_name']/a/@href").get())
            price_long = ''.join(detail.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub("\s", "", price_long)
            areas_long = ''.join(detail.xpath(".//div[contains(@class,'house_type')]//text()").getall())
            areas_long2 = re.sub("\s", "", areas_long)
            style, areas = areas_long2.split("－") if "－" in areas_long2 else ('暂无', '暂无')
            state = newhouse.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            address = detail.xpath(".//div[@class='address']/a/@title").get()

            print('名字是：', name, ori_url, '价格：', price, "面积", areas, "样式", style, "地址", address)
            item = newFangSpiderItem(province=province, city=city, name=name, ori_url=ori_url, price=price,
                                     areas=areas, style=style, state=state, address=address)
            yield item
        if response.xpath(".//div[@class='page']//a[last()]/text()").get() == "尾页":
            next_url = response.xpath(".//div[@class='page']//a[last()-1]/@href").get()
            if next_url:
                print('下一页是：', next_url)
                print('第%s页结束了' % response.xpath(".//div[@class='page']//a[@class='active']/text()").get())
                yield scrapy.Request(url=response.urljoin(next_url), callback=self.newhouse_parse, meta={
                    'info': (province, city), 'cooki': None
                })
        else:
            print("{}，{}新房爬取完毕".format(province, city))

    def esf_parse(self, response):

        print('第%s页开始了' % response.xpath(".//div[@class='page_al']//span[@class='on']/text()").get())
        state = re_cookies()  # 下载器中间件中的一个函数 用于返回selenium抓取到的cookie
        province, city = response.meta.get("info")
        if state is None:
            print("没有经过selenium")
            cooki = response.meta.get("cooki")
            # print('返回0', province, city, type(response),"coo:", cooki)
        else:
            print("经过了selenium有新cookie")
            cooki = {"Cookie": state}
            # Cookie2 = response.headers.getlist('Set-Cookie')  # 响应
            # print("第一次响应的cookie", Cookie2)
            # print('返回1', city, response.url, type(response), cooki)

        # cooki = {"cookie":"""global_cookie=dwi8uf9ky7lfteoil0w77ugjl28kjfxu44j; city=www; global_wapandm_cookie=4qqfzddnve98p4xdoo2qvct4c16kjg3r1sd; g_sourcepage=esf_fy%5Elb_pc; unique_cookie=U_n0b9vm5xw7xixtvj67lbe96cl20kjhf0ndm*2; __utma=147393320.1550169561.1609605973.1609612191.1609695300.3; __utmc=147393320; __utmz=147393320.1609695300.3.3.utmcsr=fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1609695300
        #         """}
        if response.xpath("(//div[@class='page_al']//a)[last()]/text()").get() == "尾页":
            next_url = response.xpath("(//div[@class='page_al']//a)[last()-1]/@href").get()
            if next_url:
                print('下一页是：', next_url)
                print('第%s页结束了' % response.xpath(".//div[@class='page_al']//span[@class='on']/text()").get())
                yield scrapy.Request(url=response.urljoin(next_url), headers=cooki, callback=self.esf_parse, meta={
                    'info': ("123456", city), 'cooki': cooki
                })
        else:
            print("{}，{}二手房爬取完毕".format(province, city))
