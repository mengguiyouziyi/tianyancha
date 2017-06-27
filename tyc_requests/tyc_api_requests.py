# coding:utf-8
from __future__ import print_function
import requests
import time
import re
from fake_useragent import UserAgent
try:
	from urllib import quote
except:
	from urllib.parse import quote

"""
正常来讲应该是下面这段逻辑：
	基础数据：
		用public_headers访问dis_url，获取js_url并访问，获取sgattrs；
		用api_headers访问tongji_url，获取js_code，获取token和fxck_chars；
			根据公司id首位的unicode确定sgattrs下标，构建utm；
			根据搜索关键词首字的unicode确定sgattrs下标，构建utm；
		用api_headers访问api_url获取信息。
	关系图：
		用public_headers访问public_url，获取js_url并访问，获取sgattrs；
		用api_headers访问qq_url，获取js_code，获取token和fxck_chars；
			根据公司id首位的unicode确定sgattrs下标，构建utm；
		用api_headers访问api_url获取信息。
但是现在不太正常：
	'http://www.tianyancha.com/company/24722813' 获得的 'http://static.tianyancha.com/wap/resources/scripts/app-cc33da47eb.js'和
	'http://dis.tianyancha.com/dis/old#/show?ids=24722813&cnz=true' 获得的 'http://c.tianyancha.com/vr/resources/js/c54455abc610d03451d75422cbce08bd.js'
	两个js获取到的数组相同，而且我也没有找到其他页面含有这个数组
"""


class Api(object):

	def __init__(self, type='company', id=None, keys=None):
		self.type = type
		self.id = id
		self.keys = keys

		self.session = requests.session()
		self.session.cookies.set("tnet", "36.110.41.42")

		self.ua = UserAgent()
		self.api_headers = {
			"User-Agent": self.ua.random,
			"Accept": "application/json, text/plain, */*",
			"Accept-Encoding": "gzip, deflate",
		}

		if self.type == 'company':
			# 公司
			self.tongji_url = "http://www.tianyancha.com/tongji/%s.json?random=%s" % (self.id, int(time.time()) * 1000)
			self.api_url = "http://www.tianyancha.com/v2/company/%s.json" % self.id
			self.api_headers.update({
				"Tyc-From": "normal",
				'Host': 'www.tianyancha.com',
				"Referer": "http://www.tianyancha.com/company/%s" % self.id,
			})
		elif self.type == 'search':
			# 搜索
			self.tongji_url = 'http://www.tianyancha.com/tongji/%s.json?random=%s' % (quote(self.keys), int(time.time()) * 1000)
			self.api_url = 'http://www.tianyancha.com/v2/search/%s.json?' % quote(self.keys)
			self.api_headers.update({
				"Tyc-From": "normal",
				'Host': 'www.tianyancha.com',
				"Referer": 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % quote(self.keys),
				"X-AUTH-TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzc4NDg1NTQ1NyIsImlhdCI6MTQ5ODUzNTkyNiwiZXhwIjoxNTE0MDg3OTI2fQ.QNesTsmbVo8yZGChzHelTsvIJEnoryS8TRhZONHtmhOdIaHHuX_RWJxlpqg6OvT4-f43LnhXMJ5DW40rdqIFuA",
			})
		elif self.type == 'relation':
			# 关系图
			self.tongji_url = "http://dis.tianyancha.com/qq/%s.json?random=%s" % (self.id, int(time.time()) * 1000)
			self.api_url = "http://dis.tianyancha.com/dis/getInfoById/%s.json?" % self.id
			self.api_headers.update({
				'Host': 'dis.tianyancha.com',
				'Referer': 'http://dis.tianyancha.com/dis/old'
			})
		self.sgattrs = [
			["6", "b", "t", "f", "2", "z", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y",
			 "k", "j", "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"],
			["1", "8", "o", "s", "z", "u", "n", "v", "m", "b", "9", "f", "d", "7", "h", "c", "p", "y", "2", "0", "3",
			 "j", "-", "i", "l", "k", "t", "q", "4", "6", "r", "a", "w", "5", "e", "x", "g"],
			["s", "6", "h", "0", "p", "g", "3", "n", "m", "y", "l", "d", "x", "e", "a", "k", "z", "u", "f", "4", "r",
			 "b", "-", "7", "o", "c", "i", "8", "v", "2", "1", "9", "q", "w", "t", "j", "5"],
			["x", "7", "0", "d", "i", "g", "a", "c", "t", "h", "u", "p", "f", "6", "v", "e", "q", "4", "b", "5", "k",
			 "w", "9", "s", "-", "j", "l", "y", "3", "o", "n", "z", "m", "2", "1", "r", "8"],
			["z", "j", "3", "l", "1", "u", "s", "4", "5", "g", "c", "h", "7", "o", "t", "2", "k", "a", "-", "e", "x",
			 "y", "b", "n", "8", "i", "6", "q", "p", "0", "d", "r", "v", "m", "w", "f", "9"],
			["j", "h", "p", "x", "3", "d", "6", "5", "8", "k", "t", "l", "z", "b", "4", "n", "r", "v", "y", "m", "g",
			 "a", "0", "1", "c", "9", "-", "2", "7", "q", "e", "w", "u", "s", "f", "o", "i"],
			["8", "q", "-", "u", "d", "k", "7", "t", "z", "4", "x", "f", "v", "w", "p", "2", "e", "9", "o", "m", "5",
			 "g", "1", "j", "i", "n", "6", "3", "r", "l", "b", "h", "y", "c", "a", "s", "0"],
			["d", "4", "9", "m", "o", "i", "5", "k", "q", "n", "c", "s", "6", "b", "j", "y", "x", "l", "a", "v", "3",
			 "t", "u", "h", "-", "r", "z", "2", "0", "7", "g", "p", "8", "f", "1", "w", "e"],
			["7", "-", "g", "x", "6", "5", "n", "u", "q", "z", "w", "t", "m", "0", "h", "o", "y", "p", "i", "f", "k",
			 "s", "9", "l", "r", "1", "2", "v", "4", "e", "8", "c", "b", "a", "d", "j", "3"],
			["1", "t", "8", "z", "o", "f", "l", "5", "2", "y", "q", "9", "p", "g", "r", "x", "e", "s", "d", "4", "n",
			 "b", "u", "a", "m", "c", "h", "j", "3", "v", "i", "0", "-", "w", "7", "k", "6"]]

	def get_api(self):
		# 取得token和fxckStr
		tongji_page = self.session.request("GET", self.tongji_url, headers=self.api_headers)
		js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"]["v"].split(",")])
		token = re.findall(r"token=(\w+);", js_code)[0]
		# python2不支持这个','，所以引入print_function
		print("token:", token)

		fxck_chars = re.findall(r"\'([\d\,]+)\'", js_code)[0].split(",")
		parm = self.keys if self.type == 'search' else str(self.id)
		index = int(str(ord(parm[0]))[1])
		# python2 这个下标有问题，因为中文在这是\x54，自行解决
		sogou = self.sgattrs[index]
		utm = "".join([sogou[int(fxck)] for fxck in fxck_chars])
		print("utm:", utm)

		if self.type == 'relation':
			self.session.cookies.set("rtoken", token)
			self.session.cookies.set("_rutm", utm)
		else:
			self.session.cookies.set("token", token)
			self.session.cookies.set("_utm", utm)

		api_page = self.session.request("GET", self.api_url, headers=self.api_headers)
		print(api_page.text)


if __name__ == '__main__':
    api = Api(type='company', id=24722813)
    # api = Api(type='search', keys='百度')
    # api = Api(type='relation', id=24722813)
    api.get_api()