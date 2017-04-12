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
    'tianyancha.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁止内置的中间件
}

#禁用cookies
COOKIES_ENABLES=False


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#302 Problem
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

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
