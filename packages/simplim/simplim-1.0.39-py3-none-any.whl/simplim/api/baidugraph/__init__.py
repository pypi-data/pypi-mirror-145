r"""@2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool using <https://graph.baidu.com/> & <https://ai.baidu.com/aidemo> to upload, search, download pic on BaiduGraph & detect pic on BaiduAi
"""

import requests as rq
import json

def uploadImg(fileName):
	info = open(fileName,'rb').read()
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
		'referer':'http://tools.bugscaner.com/'
	}
	res = rq.Session()
	data = {
		'tn':'pc',
		'from':'pc',
		'image_source':'PC_UPLOAD_SEARCH_FILE',
		'range':'''{'page_from': 'searchResult'}''',
	}
	files = {'image':info}
	response = res.post('https://graph.baidu.com/upload',data=data,files=files,verify=False,headers=headers)
	returndict = response.json()
	sign = returndict['data']['sign']
	url  = returndict['data']['url']
	picurl = 'https://graph.baidu.com/resource/' + sign + '.jpg'
	print('[N]', 'search url', url)
	print('[N]', 'upload to', picurl)
	return url, picurl

def uploadImg_raw(info):
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
		'referer':'http://tools.bugscaner.com/'
	}
	res = rq.Session()
	data = {
		'tn':'pc',
		'from':'pc',
		'image_source':'PC_UPLOAD_SEARCH_FILE',
		'range':'''{'page_from': 'searchResult'}''',
	}
	files = {'image':info}
	response = res.post('https://graph.baidu.com/upload',data=data,files=files,verify=False,headers=headers)
	returndict = response.json()
	sign = returndict['data']['sign']
	url  = returndict['data']['url']
	picurl = 'https://graph.baidu.com/resource/' + sign + '.jpg'
	print('[N]','search url', url)
	print('[N]','upload to',picurl)
	return url, picurl

def searchImg(fileName):
	url, picurl = uploadImg(fileName)
	if returndict['msg'] == 'Success':
		print('[N] Success, starting to sparse resource')
		page = res.get(url, headers = headers, verify = False).text
		return page
	else:
		print('[E] Upload Failed')

def detectImg_ocr(url):
	host = 'https://ai.baidu.com/aidemo'
	data = {
		'image': '',
		'image_url': url,
		'type': 'commontext',
		'detect_direction': False
	}
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
		'referer': 'https://ai.baidu.com/tech/ocr/general',
		'cookie':'PSTM=1588908167; BAIDUID=3D50572CC2497D155AAAD59A715ABFE1:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=2737C11AF0424FE96F10064E74658ECF; MCITY=-158%3A218%3A; H_PS_PSSID=1450_31669_21080_31253_31596_31605_31271_31463_30823; BDUSS=0tSQzdXcmhVVjJZS0F4eXVMVXFzT3ROam1xVFNnVHlRSkwxdGt-S3l2LTA0TzVlRUFBQUFBJCQAAAAAAAAAAAEAAADnS~xbydnE6sjyzcEwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALRTx160U8dec; delPer=0; PSINO=6; BCLID=7276149949773063458; BDSFRCVID=NtCOJeC62rw_J0ouvkQ5MRVUqfaPqNOTH6aImWQbBlut1nDH8-cBEG0P_x8g0K4bo7k0ogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRAOoC8ytDvjDb7GbKTD-tFO5eT22-usL6bC2hcH0KLKJbOLhlb85JKHhJ5uQq5P-mTb0RT7tMb1MRjvWljO3-uhMt-eWbQUKmLJXq5TtUJoSDnTDMRhqqJXqqjyKMniBIv9-pnGBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuD6K5j65XDGLs54JJ26c0LPI82P5Hfn5Y-Pvo5t3H-UnLq-J20mOZ0l8Ktt5voCOtjJo-hx-4XJ5pLRopJg3ZKl7mWIQHDPThefRhe5LSKtoAaUvZKJv4KKJxaMKWeIJo5t5BMh8shUJiBM7MBan7-lRIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC_wj50WjTjXeUQ0eJcybCnKW5rJabC3jb7cXU6qLT5Xj4LJbTDqb6cXKqjzLfQlqJcx0qjxjl0njxQyJUcI3ejIX4cqKKJqVnrj-xonDh8ebG7MJUntKHLOK-oO5hvv8b3O3M7lXMKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_EJjDeJJFHoDDQKROMjtQY5bu_MbL_5Uo05-7ybCPX3b7EfMj6Oq7_bf--DRLUWG-eQJQq22Jt2xoCQ4jqOpvRy-bxy5K_hUvd0t3vaHneBfQx2pnkH45HQT3mhpQbbN3i-4j82NRMWb3cWhRJ8UbS3fvPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JD-50eGLOt6FjJRC8VbOsa-5fK4bNh4bqhR3H-UnLqM6J02OZ0l8Kttob_pFxhno-Mpo0XJ5pLRohKGRD2q7mWIQHOJ650t5IhbL3DfTRBTkLK2r4KKJxX-PWeIJoj-5ojPnQhUJiBM7MBan7-lRIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbRO4-TF5D5cBjfK; Hm_lvt_8b973192450250dd85b9011320b455ba=1590135564; Hm_lpvt_8b973192450250dd85b9011320b455ba=1590135919; __yjsv5_shitong=1.0_7_e61573df99b73a5e533b43fc32a9e83c649c_300_1590135919175_119.98.201.42_1f73e379'
	}
	try:
		response = rq.post(url=host, data=data, headers=headers).json()
	except:
		return -1
	# print('[R]',response)
	if response['msg']=='success':
		data = response['data']
		words = []
		string = ''
		for word in data['words_result']:
			words.append(word['words'])
			string += word['words']
		print('[N]','string',string)
		return words, string
	else: 
		return -1





















