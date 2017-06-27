# coding:utf-8
from __future__ import print_function, unicode_literals
import requests
import time
import re
import json

"""
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
"""


class Api(object):

	def __init__(self, type='company', id=None, keys=None):
		self.type = type
		self.id = id
		self.keys = keys

		self.session = requests.session()
		self.session.cookies.set("tnet", "36.110.41.42")
		self.public_headers = {
			"User-Agent": "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
		}
		self.api_headers = self.public_headers.copy()
		self.api_headers.update({
			"Accept": "application/json, text/plain, */*",
			"Accept-Encoding": "gzip, deflate",
		})

		if self.type == 'company':
			# dis_url = "http://dis.tianyancha.com/dis/old#/show?ids=24722813&cnz=true"
			# # 基本信息
			self.tongji_url = "http://www.tianyancha.com/tongji/%s.json?random=%s" % (self.id, int(time.time()) * 1000)
			self.api_url = "http://www.tianyancha.com/v2/company/%s.json" % self.id
			self.api_headers.update({
				"Tyc-From": "normal",
				'Host': 'www.tianyancha.com',
				"Referer": "http://www.tianyancha.com/company/%s" % self.id,
			})
		elif self.type == 'search':
			# 搜索
			self.tongji_url = 'http://www.tianyancha.com/tongji/%s.json?random=1498540458717' % self.keys
			self.api_url = 'http://www.tianyancha.com/v2/search/%s.json?' % self.keys
			self.api_headers.update({
				"Tyc-From": "normal",
				'Host': 'www.tianyancha.com',
				"Referer": 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % self.keys,
				# "CheckError": "check",
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



	def get_api(self):

		# 访问首页
		# dis_page = session.request("GET", dis_url, headers=public_headers)

		# 访问js取出 _sgAtt
		# js_url = re.findall(r"http.+?c\.tianyancha\.com/vr/resources/js/\w+\.js", dis_page.content.decode('utf-8'))[0]
		# js_page = session.request("GET", js_url, headers=public_headers)
		# sgattrs = json.loads(re.findall(r"n\._sgArr=(.+?);", js_page.content.decode('utf-8'))[0])
		sgattrs = [
			["6", "b", "t", "f", "2", "z", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y", "k", "j", "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"],
			["1", "8", "o", "s", "z", "u", "n", "v", "m", "b", "9", "f", "d", "7", "h", "c", "p", "y", "2", "0", "3", "j", "-", "i", "l", "k", "t", "q", "4", "6", "r", "a", "w", "5", "e", "x", "g"],
			["s", "6", "h", "0", "p", "g", "3", "n", "m", "y", "l", "d", "x", "e", "a", "k", "z", "u", "f", "4", "r", "b", "-", "7", "o", "c", "i", "8", "v", "2", "1", "9", "q", "w", "t", "j", "5"],
			["x", "7", "0", "d", "i", "g", "a", "c", "t", "h", "u", "p", "f", "6", "v", "e", "q", "4", "b", "5", "k", "w", "9", "s", "-", "j", "l", "y", "3", "o", "n", "z", "m", "2", "1", "r", "8"],
			["z", "j", "3", "l", "1", "u", "s", "4", "5", "g", "c", "h", "7", "o", "t", "2", "k", "a", "-", "e", "x", "y", "b", "n", "8", "i", "6", "q", "p", "0", "d", "r", "v", "m", "w", "f", "9"],
			["j", "h", "p", "x", "3", "d", "6", "5", "8", "k", "t", "l", "z", "b", "4", "n", "r", "v", "y", "m", "g", "a", "0", "1", "c", "9", "-", "2", "7", "q", "e", "w", "u", "s", "f", "o", "i"],
			["8", "q", "-", "u", "d", "k", "7", "t", "z", "4", "x", "f", "v", "w", "p", "2", "e", "9", "o", "m", "5", "g", "1", "j", "i", "n", "6", "3", "r", "l", "b", "h", "y", "c", "a", "s", "0"],
			["d", "4", "9", "m", "o", "i", "5", "k", "q", "n", "c", "s", "6", "b", "j", "y", "x", "l", "a", "v", "3", "t", "u", "h", "-", "r", "z", "2", "0", "7", "g", "p", "8", "f", "1", "w", "e"],
			["7", "-", "g", "x", "6", "5", "n", "u", "q", "z", "w", "t", "m", "0", "h", "o", "y", "p", "i", "f", "k", "s", "9", "l", "r", "1", "2", "v", "4", "e", "8", "c", "b", "a", "d", "j", "3"],
			["1", "t", "8", "z", "o", "f", "l", "5", "2", "y", "q", "9", "p", "g", "r", "x", "e", "s", "d", "4", "n", "b", "u", "a", "m", "c", "h", "j", "3", "v", "i", "0", "-", "w", "7", "k", "6"]]

		# 取得token和fxckStr
		tongji_page = self.session.request("GET", qq_url, headers=api_headers)
		js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"]["v"].split(",")])
		"""
		!function(n){document.cookie='token=ceb3e519ca13481fbb69a7b88310b17c;path=/;';n.wtf=function(){return'36,16,23,28,28,7,28,25,5,11,5,8,19,34,21,16,11,8,23,7,21,31,5,31,21,25,31,0,36,23,11,8'}}(window);
		if(window.wtf){var fxck = window.wtf().split(",");var fxckStr = "";for(var i=0;i<fxck.length;i++){fxckStr+=window.$SoGou$[fxck[i]];}document.cookie = "_utm="+fxckStr+";path=/;";window.wtf = null;}
		"""
		token = re.findall(r"token=(\w+);", js_code)[0]
		print("token:", token)

		fxck_chars = re.findall(r"\'([\d\,]+)\'", js_code)[0].split(",")
		index = int(str(ord(str(id)[0]))[1])
		# index = int(str(ord(keys[0]))[1])
		sogou = sgattrs[index]
		"""
		sogou = json.loads(re.findall(r"window.\$SoGou\$=(.+?),function", js_page.content.decode('utf-8'))[0])
		window.$SoGou$=["j","p","7","o","3","w","0","-","2","e","9","z","f","m","b","k","u","8","g","s","a","1","d","y","r","i","h","q","l","n","v","6","5","c","x","4","t"],function(e,t)
		"""
		utm = "".join([sogou[int(fxck)] for fxck in fxck_chars])  # if(window.wtf){var fxck = window.wtf().split(",");var fxckStr = "";for(var i=0;i<fxck.length;i++){fxckStr+=window.$SoGou$[fxck[i]];}document.cookie = "_utm="+fxckStr+";path=/;";window.wtf = null;}
		print("utm:", utm)

		self.session.cookies.set("rtoken", token)
		self.session.cookies.set("_rutm", utm)

		# r = session.request("GET", "http://www.tianyancha.com/IcpList/24722813.json", headers=api_headers)
		# print(r.content)

		api_page = self.session.request("GET", api_url, headers=api_headers)
		print(api_page.content)
