# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import codecs


class GetCompanySpider(CrawlSpider):
    name = 'get_company'
    allowed_domains = ['www.tianyancha.com']

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.tianyancha.com',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://www.tianyancha.com/search',
        }
        url = 'http://www.tianyancha.com/search?key=酒钢宏兴&checkFrom=searchBox'
        yield scrapy.FormRequest(url, headers=headers, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(response.url)
        # self.logger.info(response.body_as_unicode())
        print(response.xpath('//a[@class="query_name search-new-color"]/@href').extract())
        with codecs.open('search酒钢宏兴.html', 'wb', 'utf-8') as file:
            file.writelines(response.body_as_unicode())
