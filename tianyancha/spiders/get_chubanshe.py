# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import codecs
import os


class GetCompanySpider(CrawlSpider):
    name = 'get_chubanshe'
    allowed_domains = ['www.tianyancha.com']

    def __init__(self):
        company_path = os.path.join(os.getcwd(), 'chubanshe.txt')
        with codecs.open(company_path, 'r', 'utf-8') as f:
            self.company_list = f.readlines()

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
        urls = ['http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % str(self.company).strip() for self.company in self.company_list]
        for url in urls:
            print('request----url----：' + url)
            yield scrapy.Request(url, headers=headers, callback=self.parse_item)

    def parse_item(self, response):
        print('response----url----：' + response.url)
        # self.logger.info(response.body_as_unicode())
        company_url_list = response.xpath('//a[contains(@class, "query_name") and contains(@class, "search-new-color")]/@href').extract()
        # print('获取得到的公司url列表：' + str(company_url_list))
        if len(company_url_list) > 0:
            desired_url = company_url_list[0]
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%s~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' % desired_url)
            with codecs.open('chubanshe_url_list.txt', 'ab', 'utf-8') as file:
                file.write(desired_url + '\n')
        else:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~获取查询列表为空~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            with codecs.open('chubanshe_empty.txt', 'ab', 'utf-8') as file:
                file.write(self.company + '\n')




        # with codecs.open('%s.html' % str(self.company), 'wb', 'utf-8') as file:
        #     file.writelines(response.body_as_unicode())
