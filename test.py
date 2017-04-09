# -*- coding: utf-8 -*-
start_url = ['http://www.yz21.org/stock/info/']
print(start_url)
next_link = ['http://www.yz21.org/stock/info/stocklist_%d.html' % page for page in range(2,166)]
print(next_link)
start_url.extend(next_link)
print(start_url)