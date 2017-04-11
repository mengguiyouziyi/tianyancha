# -*- coding: utf-8 -*-

# Scrapy settings for tianyancha project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tianyancha'

SPIDER_MODULES = ['tianyancha.spiders']
NEWSPIDER_MODULE = 'tianyancha.spiders'

DOWNLOADER_MIDDLEWARES = {
    'tianyancha.middlewares.ProxyMiddleware': 100,#代理中间件
    'tianyancha.middlewares.RotateUserAgentMiddleware': 200,#请求头中间件
    # 'twitterspider.middleware.CheckMiddleware': 300,#检测爬虫状态码,解决302重定向
    'tianyancha.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁止内置的中间件
}

#数据库管道处理
# ITEM_PIPELINES = {
#     'twitterspider.pipelines.JsonWriterPipeline': 300
# }
# 代理设置
# PROXIES = [
#     {'ip_port': '122.5.131.146:808','user_pass':''},
#     {'ip_port': '115.220.149.251:808','user_pass':''},
#     {'ip_port': '113.123.76.221:808','user_pass':''},
#     {'ip_port': '27.159.126.36:8118','user_pass':''},
# ]

# DEFAULT_REQUEST_HEADERS = {
#     'Host': 'www.yz21.org',
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Upgrade-Insecure-Requests': '1',
#     # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
#     'Referer': 'http://www.yz21.org/stock/info/',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     # 'Cookie': '__utma=165984246.1321744277.1491733231.1491733231.1491733231.1; __utmc=165984246; __utmz=165984246.1491733231.1.1.utmccn=(organic)|utmcsr=baidu|utmctr=|utmcmd=organic; __utmb=165984246',
#     # 'If-Modified-Since': 'Fri, 07 Apr 2017 11:10:04 GMT',
#
#     # 'Referer': "https://www.google.com/"
# }
#禁用cookies
COOKIES_ENABLES=False
# SPIDER_MIDDLEWARES = {
# 'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
# }
#Twitter~API
# TWITTER_CONSUMER_KEY        = 'SbouzZVBRKwHUjjxfx2zYjo18'
# TWITTER_CONSUMER_SECRET     = 'NNm6hr0UKOcdHoyoHxPwLzlX3uXcXMKXyyjCcQ9B6ajIoSBJzl'
# TWITTER_ACCESS_TOKEN_KEY    = '839305580153974784-kjyjO3I0xheNK8NmvboSaTM2pn6Z0ts'
# TWITTER_ACCESS_TOKEN_SECRET = 'jJhF8xTgdtVs0lnIq2UDbbP6dS0ASr412IdIRZquwQHHR'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twitterspider (+http://www.yourdomain.com)'

# Obey robots.txt rules

ROBOTSTXT_OBEY = False
#302 Problem
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2  # 间隔时间,两次下载的间隔
RANDOMIZE_DOWNLOAD_DELAY = True  # 开启随机延迟

USER_AGENT_CHOICES = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
]


LOG_STDOUT = True







# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyancha (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tianyancha.middlewares.TianyanchaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tianyancha.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tianyancha.pipelines.TianyanchaPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
