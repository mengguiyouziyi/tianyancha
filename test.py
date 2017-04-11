# -*- coding: utf-8 -*-
# start_url = ['http://www.yz21.org/stock/info/']
# print(start_url)
# next_link = ['http://www.yz21.org/stock/info/stocklist_%d.html' % page for page in range(2,166)]
# print(next_link)
# start_url.extend(next_link)
# print(start_url)

# 2016-12-29 16:55:34 [scrapy] INFO: Scrapy 1.1.1 started (bot: weibo)
# 2016-12-29 16:55:34 [scrapy] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'weibo.spiders', 'CONCURRENT_REQUESTS_PER_DOMAIN': 16, 'CONCURRENT_REQUESTS': 32, 'SPIDER_MODULES': ['weibo.spiders'], 'AUTOTHROTTLE_START_DELAY': 10, 'CONCURRENT_REQUESTS_PER_IP': 16, 'BOT_NAME': 'weibo', 'RETRY_TIMES': 5, 'COOKIES_ENABLED': False, 'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 403, 414], 'TELNETCONSOLE_ENABLED': False, 'AUTOTHROTTLE_ENABLED': True, 'DOWNLOAD_DELAY': 2}
# 2016-12-29 16:55:34 [py.warnings] WARNING: /Users/brucedone/anaconda/envs/scrapy3/lib/python2.7/site-packages/scrapy/utils/deprecate.py:156: ScrapyDeprecationWarning: `scrapy.telnet.TelnetConsole` class is deprecated, use `scrapy.extensions.telnet.TelnetConsole` instead
#   ScrapyDeprecationWarning)
#
# 2016-12-29 16:55:34 [scrapy] INFO: Enabled extensions:
# ['scrapy.extensions.logstats.LogStats',
#  'scrapy.extensions.corestats.CoreStats',
#  'scrapy.extensions.throttle.AutoThrottle']
# 2016-12-29 16:55:35 [scrapy] INFO: Enabled downloader middlewares:
# ['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
#  'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
#  'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
#  'scrapy.downloadermiddlewares.retry.RetryMiddleware',
#  'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
#  'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
#  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
#  'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
#  'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware',
#  'scrapy.downloadermiddlewares.stats.DownloaderStats']
# 2016-12-29 16:55:35 [scrapy] INFO: Enabled spider middlewares:
# ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
#  'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
#  'scrapy.spidermiddlewares.referer.RefererMiddleware',
#  'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
#  'scrapy.spidermiddlewares.depth.DepthMiddleware']
# 2016-12-29 16:55:35 [scrapy] INFO: Enabled item pipelines:
