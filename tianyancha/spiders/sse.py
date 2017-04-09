# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import codecs


class SseSpider(CrawlSpider):
    name = 'yz21'
    allowed_domains = ['www.yz21.org']
    def start_requests(self):
        headers = {
            'Host': 'www.yz21.org',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Referer': 'http://www.yz21.org/stock/info/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Cookie': '__utma=165984246.1321744277.1491733231.1491733231.1491733231.1; __utmc=165984246; __utmz=165984246.1491733231.1.1.utmccn=(organic)|utmcsr=baidu|utmctr=|utmcmd=organic; __utmb=165984246',
            # 'If-Modified-Since': 'Fri, 07 Apr 2017 11:10:04 GMT',

            # 'Referer': "https://www.google.com/"
        }
        # start_urls = ['http://www.yz21.org/stock/info/', 'http://www.yz21.org/stock/info/stocklist_2.html']
        start_urls = ['http://www.yz21.org/stock/info/']
        for link in start_urls:
            yield scrapy.Request(link, headers=headers, callback=self.parse_item)

        next_link = ['http://www.yz21.org/stock/info/stocklist_%d.html' % page for page in range(3,166)]
        # start_urls.extend(next_link)
        # for index, link in enumerate(next_link):
        #     # print('------------%d--------------' % index)# 17===3
        #     headers.update({'Referer': ('http://www.yz21.org/stock/info/stocklist_%d.html' % (index + 2))})
        #     yield scrapy.Request(link, headers=headers, callback=self.parse_item)

    # rules = (
    #     Rule(LinkExtractor(allow=r''),
    #          callback='parse_item',
    #          follow=True),
    # )

    def parse_item(self, response):
        # with codecs.open('yz21_1.html', 'wb', 'utf-8') as file:
        #     file.writelines(response.body_as_unicode())
        # .//*[@id='All_stocks1_DataGrid1']/tbody/tr/td[4]/a/text()
        print(response.xpath("//tbody"))
        # self.logger.info(response.body_as_unicode())
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
