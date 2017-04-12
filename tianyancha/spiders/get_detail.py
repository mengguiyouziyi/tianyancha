# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import codecs


class GetDetailSpider(CrawlSpider):
    name = 'get_detail'
    allowed_domains = ['www.tianyancha.com']
    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.tianyancha.com',
            #'Origin': 'http://www.tianyancha.com',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': 'http://www.tianyancha.com/search?key=阿鲁科尔沁旗西古井子兴盛农牧专业合作社&checkFrom=searchBox',
            'Referer': 'https://www.google.com/',
        }
        url = 'http://www.tianyancha.com/company/2998583730'
        yield scrapy.FormRequest(url, headers=headers, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(response.url)
        self.logger.info(response.body_as_unicode())
        with codecs.open('2998583730.html', 'wb', 'utf-8') as file:
            file.writelines(response.body_as_unicode())
