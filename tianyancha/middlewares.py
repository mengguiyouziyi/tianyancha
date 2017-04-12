# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from random import choice
from scrapy import signals
from scrapy.exceptions import NotConfigured
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import random
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs
import os

class ProxyMiddleware(object):
    def __init__(self):
        self.proxys = []
        ip_path = os.path.join(os.getcwd(), 'ip_list.txt')
        with codecs.open(ip_path, 'r', 'utf-8') as f:
            self.ip_list = f.readlines()
            for ip in self.ip_list:
                self.proxy = {'ip_port': str(ip).strip(),'user_pass':b''}
                # print(self.proxy)
                self.proxys.append(self.proxy)

    def process_request(self, request, spider):
        self.proxy = random.choice(self.proxys)
        if self.proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % self.proxy['ip_port']
            request.meta['proxy'] = "https://%s" % self.proxy['ip_port']
            encoded_user_pass = base64.b64encode(self.proxy['user_pass'])
            request.headers['Proxy-Authorization'] = b'Basic ' + encoded_user_pass
            print("**************ProxyMiddleware have pass************" + self.proxy['ip_port'])
        else:
            print("**************ProxyMiddleware no pass************" + self.proxy['ip_port'])
            request.meta['proxy'] = "http://%s" % self.proxy['ip_port']

    def process_response(self, request, response, spider):
        response_status = response.status
        request_url = request.url
        if response_status == 200:
            print(self.proxy['ip_port'] + '：代理ip正常················')
            return response
        else:
            print(self.proxy['ip_port'] + '：代理ip不能用了··············')
            self.proxys.pop(self.proxy)
            self.process_request(self, request.replace(url=request_url), spider)


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        print("PhantomJS is starting...")
        driver = webdriver.PhantomJS() #指定使用的浏览器
        driver.get(request.url)
        if spider.name == "get_detail":
            # driver = webdriver.Firefox()
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(10)
            body = driver.page_source
            # print("访问"+request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        elif spider.name == 'get_company':
            try:
                element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-xs-10.search_repadding2.f18')))
            except Exception as e:
                print('没有找到元素或发生其他异常' + e)
            finally:
                # print(driver.find_element_by_xpath('//a[@class="query_name search-new-color"]/@href').text())
                # driver.close()
                body = driver.page_source
                # print("访问" + request.url)
                return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


class RotateUserAgentMiddleware(object):
    """Middleware used for rotating user-agent for each request"""
    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        """Get user agents from settings.py"""
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])
        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")
        ret = cls(user_agents)
        crawler.signals.connect(ret.spider_opened, signal=signals.spider_opened)
        return ret

    def spider_opened(self, spider):
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        """Select user agent randomly on request"""
        if self.enabled and self.user_agents:
            request.headers['user-agent'] = choice(self.user_agents)



# class TianyanchaSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
