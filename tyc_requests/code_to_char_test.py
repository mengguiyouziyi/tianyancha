# coding:utf-8

def strfromcode(strcode):
	arr = strcode.split(",")
	stringfromcode1 = ""
	for lin in arr:
		stringfromcode1 += chr(int(lin))
	return stringfromcode1


if __name__ == '__main__':
	# stringfromcode1 = strfromcode('33,102,117,110,99,116,105,111,110,40,110,41,123,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,61,39,116,111,107,101,110,61,99,101,98,51,101,53,49,57,99,97,49,51,52,56,49,102,98,98,54,57,97,55,98,56,56,51,49,48,98,49,55,99,59,112,97,116,104,61,47,59,39,59,110,46,119,116,102,61,102,117,110,99,116,105,111,110,40,41,123,114,101,116,117,114,110,39,51,54,44,49,54,44,50,51,44,50,56,44,50,56,44,55,44,50,56,44,50,53,44,53,44,49,49,44,53,44,56,44,49,57,44,51,52,44,50,49,44,49,54,44,49,49,44,56,44,50,51,44,55,44,50,49,44,51,49,44,53,44,51,49,44,50,49,44,50,53,44,51,49,44,48,44,51,54,44,50,51,44,49,49,44,56,39,125,125,40,119,105,110,100,111,119,41,59')
	# stringfromcode1 = strfromcode('33,102,117,110,99,116,105,111,110,40,110,41,123,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,61,39,114,116,111,107,101,110,61,55,56,55,56,51,97,100,102,51,101,54,54,52,54,52,99,97,97,98,50,53,101,102,51,50,98,56,54,97,51,52,48,59,112,97,116,104,61,47,59,39,59,110,46,119,116,102,61,102,117,110,99,116,105,111,110,40,41,123,114,101,116,117,114,110,39,49,50,44,49,53,44,57,44,49,49,44,49,56,44,49,53,44,49,48,44,49,44,49,53,44,51,49,44,57,44,50,56,44,50,56,44,51,49,44,49,53,44,51,49,44,49,44,57,44,51,52,44,49,49,44,49,49,44,49,53,44,49,44,57,44,51,52,44,49,51,44,50,48,44,48,44,50,48,44,49,51,44,49,50,44,49,48,39,125,125,40,119,105,110,100,111,119,41,59')
	"""!function(n){document.cookie='rtoken=78783adf3e66464caab25ef32b86a340;path=/;';n.wtf=function(){return'12,15,9,11,18,15,10,1,15,31,9,28,28,31,15,31,1,9,34,11,11,15,1,9,34,13,20,0,20,13,12,10'}}(window);"""
	# stringfromcode1 = strfromcode('105,102,40,119,105,110,100,111,119,46,119,116,102,41,123,118,97,114,32,102,120,99,107,32,61,32,119,105,110,100,111,119,46,119,116,102,40,41,46,115,112,108,105,116,40,34,44,34,41,59,118,97,114,32,102,120,99,107,83,116,114,32,61,32,34,34,59,102,111,114,40,118,97,114,32,105,61,48,59,105,60,102,120,99,107,46,108,101,110,103,116,104,59,105,43,43,41,123,102,120,99,107,83,116,114,43,61,119,105,110,100,111,119,46,36,83,111,71,111,117,36,91,102,120,99,107,91,105,93,93,59,125,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,32,61,32,34,95,117,116,109,61,34,43,102,120,99,107,83,116,114,43,34,59,112,97,116,104,61,47,59,34,59,119,105,110,100,111,119,46,119,116,102,32,61,32,110,117,108,108,59,125')
	# li = [
	# 	'119,105,110,100,111,119,46,36,83,111,71,111,117,36,32,61,32,119,105,110,100,111,119,46,95,115,103,65,114,114,91,%d,93' % d
	# 	for d in range(48, 58)]
	# for l in li:
	# 	stringfromcode1 = strfromcode(l)
	# 	print(stringfromcode1)
	str1 = '''33,102,117,110,99,116,105,111,110,40,110,41,123,100,111,99,117,109,101,110,116,46,99
,111,111,107,105,101,61,39,116,111,107,101,110,61,100,49,53,49,54,52,50,97,100,55,53,98,52,57,51,49,56
,97,57,102,57,51,50,51,102,55,51,49,49,55,49,100,59,112,97,116,104,61,47,59,39,59,110,46,119,116,102
,61,102,117,110,99,116,105,111,110,40,41,123,114,101,116,117,114,110,39,50,57,44,49,48,44,52,44,52,44
,55,44,52,44,55,44,51,48,44,49,50,44,50,57,44,52,44,51,53,44,55,44,51,48,44,50,50,44,49,50,44,51,54,44
,51,54,44,50,52,44,49,57,44,51,54,44,51,48,44,49,53,44,50,50,44,51,53,44,56,44,49,50,44,51,48,44,49,57
,44,56,44,50,54,44,49,57,39,125,125,40,119,105,110,100,111,119,41,59'''
	stringfromcode1 = strfromcode(str1)
	print(stringfromcode1)
