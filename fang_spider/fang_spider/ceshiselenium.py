import random , time
from selenium import webdriver
class se:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # print("这是总的某个城市页面链接",request.url)
        self.driver.get("https://esf.fang.com")
        # self.driver.get(request.url)
        time.sleep(2)
        cookies = self.driver.get_cookies()
        cookies_list = []
        for cookie_dict in cookies:
            cookie = cookie_dict['name'] + '=' + cookie_dict['value']
            cookies_list.append(cookie)
        # print(cookies_list)
        header_cookie = ';'.join(cookies_list)
        print("这是二手房某城市初始页面的cookie:",header_cookie)
        # request.headers["cookie"] = header_cookie
        self.driver.quit()
se()