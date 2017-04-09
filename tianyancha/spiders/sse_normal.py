# -*- coding: utf-8 -*-
import scrapy
import codecs


class SseNormalSpider(scrapy.Spider):
    name = "yz21_normal"
    allowed_domains = ["www.yz21.org"]
    link_list = ['http://www.yz21.org/stock/info/stocklist_%d.html' % page for page in range(2, 166)]
    start_url = ['http://www.yz21.org/stock/info/']
    start_url.extend(link_list)

    def parse(self, response):
        print(self.start_url)
        print(response.url)
        # with codecs.open('yz21_normal.html', 'wb', 'utf-8') as file:
        #     file.writelines(response.body_as_unicode())
