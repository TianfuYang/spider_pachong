# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random , time
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.chrome.options import Options

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class FangSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FangSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
        "ozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36"
    ]

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # print("有cookie吗", request.headers.getlist("cookie"))
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # cook = """global_cookie=dwi8uf9ky7lfteoil0w77ugjl28kjfxu44j; city=www; global_wapandm_cookie=4qqfzddnve98p4xdoo2qvct4c16kjg3r1sd; g_sourcepage=esf_fy%5Elb_pc; unique_cookie=U_n0b9vm5xw7xixtvj67lbe96cl20kjhf0ndm*2; __utma=147393320.1550169561.1609605973.1609612191.1609695300.3; __utmc=147393320; __utmz=147393320.1609695300.3.3.utmcsr=fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1609695300
        # """
        # if request.headers.getlist("cookie"):
        #     print("有cookie",request.headers.getlist("Cookie"))
        #     request.headers["cookie"] = cook
        #     request.headers["cookie"] = request.headers.getlist("Cookie")[0].decode("utf8")
        useragent = random.choice(self.user_agent)
        request.headers["User-Agent"] = useragent
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


re_cookie = ''  # 该变量用于存储selenium 返回的COOKIE

# 下面是selenium程序 用于获取cookie


class ErShouFangSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # def __init__(self):

    def process_request(self, request, spider):
        if "esf" in request.url and "house/i" not in request.url:
            global re_cookie
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 设置为无头浏览器
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            print("这是selenium中总的某个城市页面链接",request.url)
            self.driver.get("https://www.fang.com")
            self.driver.get(request.url)
            time.sleep(2)
            cookie = self.driver.get_cookies()
            # print("这是请求到的原始cookie",cookie)
            cookies_list = []
            for cookie_dict in cookie:
                cookie = cookie_dict['name'] + '=' + cookie_dict['value']
                cookies_list.append(cookie)
            # print("拼接后的cookir",cookies_list)
            cookies = ';'.join(cookies_list)
            # print("这是二手房某城市初始页面的cookie:",cookies)
            # request.headers["cookie"] = header_cookie
            source = self.driver.page_source
            # print("获取到的类型为",type(source))
            response = HtmlResponse(url=self.driver.current_url, body=source, request=request,encoding='utf8')
            self.driver.quit()
            re_cookie = cookies
            return response
        else:
            return None
def re_cookies():
    global re_cookie
    re_cookie2 = re_cookie
    re_cookie = None
    # print("我被调用了，来给你发返回cook值",re_cookie2)
    return re_cookie2
