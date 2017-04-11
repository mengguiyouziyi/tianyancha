# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import codecs


class GetDetailSpider(CrawlSpider):
    name = 'get_detail'
    allowed_domains = ['www.tianyancha.com']
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES' : {
    #         'tianyancha.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
    #     }
    # }
    # start_urls = ['http://www.tianyancha.com/company/137874593/']
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
            #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        url = 'http://www.tianyancha.com/company/2998583730'
        yield scrapy.FormRequest(url, headers=headers, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(response.url)
        self.logger.info(response.body_as_unicode())
        with codecs.open('2998583730.html', 'wb', 'utf-8') as file:
            file.writelines(response.body_as_unicode())
        # i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
