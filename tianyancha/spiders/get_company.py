# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import codecs


class GetCompanySpider(CrawlSpider):
    name = 'get_company'
    allowed_domains = ['www.tianyancha.com']
    # start_urls = ['http://www.tianyancha.com/search/']

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.tianyancha.com',
            #'Origin': 'http://www.tianyancha.com',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://www.tianyancha.com/search',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        url = 'http://www.tianyancha.com/search?key=603208&checkFrom=searchBox'
        yield scrapy.FormRequest(url, headers=headers, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(response.url)
        self.logger.info(response.body_as_unicode())
        with codecs.open('search603208.html', 'wb', 'utf-8') as file:
            file.writelines(response.body_as_unicode())
