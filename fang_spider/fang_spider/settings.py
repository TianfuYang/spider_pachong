# Scrapy settings for fang_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fang_spider'

SPIDER_MODULES = ['fang_spider.spiders']
NEWSPIDER_MODULE = 'fang_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fang_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 当COOKIES_ENABLED是注释的时候scrapy默认没有开启cookie
# 设置为False时 默认使用该settings文件里的cookie。其他通过cookies设置的cookie无效 但是headers里可以继续设置
# 当COOKIES_ENABLED设置为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie

COOKIES_ENABLED = False
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en',
    "accept-encoding":"gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
#     "upgrade-insecure-requests": 1,
#     'cookie': """global_cookie=dwi8uf9ky7lfteoil0w77ugjl28kjfxu44j; city=www; global_wapandm_cookie=4qqfzddnve98p4xdoo2qvct4c16kjg3r1sd; g_sourcepage=esf_fy%5Elb_pc; unique_cookie=U_n0b9vm5xw7xixtvj67lbe96cl20kjhf0ndm*2; __utma=147393320.1550169561.1609605973.1609612191.1609695300.3; __utmc=147393320; __utmz=147393320.1609695300.3.3.utmcsr=fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1609695300
# """
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'fang_spider.middlewares.FangSpiderSpiderMiddleware': 500,
   # 'fang_spider.middlewares.FangSpiderDownloaderMiddleware': 200,

}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'fang_spider.middlewares.FangSpiderDownloaderMiddleware': 200,
   'fang_spider.middlewares.ErShouFangSpiderDownloaderMiddleware': 150,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'fang_spider.pipelines.newFangSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
