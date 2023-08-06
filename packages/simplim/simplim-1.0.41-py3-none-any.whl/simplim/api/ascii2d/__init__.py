r"""@2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool using website <https://ascii2d.net/> & its search method <https://ascii2d.net/search/uri> to search & match anime pics which are mostly on Pixiv
"""

from bs4 import BeautifulSoup as bs
import simplim.api.translate.youdao as yd
from pathlib import Path
import requests as rq
import json
import re

host = 'https://ascii2d.net/'

url = 'http://tiebapic.baidu.com/forum/w%3D580/sign=5ab18faec02a60595210e1121835342d/f94dbade9c82d158c7013ad6970a19d8bd3e429d.jpg'

headers = {
	'origin': 'https://ascii2d.net',
	'referer': 'https://ascii2d.net/',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

cookie = {
	'_session_id': '79565ed210ce8fcd11c72d20b8651189'
}

def getPage(url):
	data = {
		'authenticity_token': 'MY2WYZuFTuosuWtloftEIDs6NeA16P1F8FgNiUqI/kFDoetkQHzyxT8O2yC2I5cGcwTynFvewBuVB/JN7IQeTQ==',
		'uri': url,
		'utf-8': '✓',
		'search': ''
	}
	response = rq.post(url = 'https://ascii2d.net/search/uri', headers = headers, data = data, cookies = cookie)
	text = response.text
	url = response.url
	hash_self = url[re.search('color\/',url).end():]
	items = bs(text,'lxml').find_all(class_='row')[2].find_all(class_='item-box')
	final_results = []
	
	for item in items:
		thumbnail = host + item.find(class_='image-box').find('img').get('src')
		info = item.find(class_='info-box')
		hash_ = info.find(class_ = 'hash').text
		img_detail = info.find('small').text.split(' ')
		img_size = img_detail[0]
		start = re.search('x',img_size).start()
		width = img_size[:start]
		height = img_size[start+1:]
		img_type = img_detail[1]
		file_size = img_detail[2]
		detail = item.find(class_='detail-box')
		results = []
		if detail.text!='\n' and detail.text!='':
			site = detail.find('small').text
			if re.search('twitter',site):
				site = 'twitter'
			elif re.search('pixiv',site):
				site = 'pixiv'
			elif re.search('ニコニコ静画',site):
				site = 'ニコニコ静画'
			links = detail.find_all('a')
			for count in range(0, int(len(links)/2)):
				text1 = links[count*2].text
				text2 = links[count*2+1].text
				link1 = links[count*2].get('href')
				link2 = links[count*2+1].get('href')
				if site == 'twitter':
					results.append({
						'time': text1.split('.'),
						'work': link1,
						'user_name': text2,
						'user_link': link2,
						'user_id': link2[re.search('user_id=', link2).end():]
						})
				elif site == 'pixiv':
					results.append({
						'name': text1,
						'work': link1,
						'work-id': link1[re.search('artworks\/', link1).end():],
						'user_name': text2,
						'user_link': link2,
						'user_id': link2[re.search('users\/', link2).end():]
						})
				elif site == 'ニコニコ静画':
					results.append({
						'name': text1,
						'work': link1,
						'work-id': link1[re.search('seiga\/', link1).end():],
						'user_name': text2,
						'user_link': link2,
						'user_id': link2[re.search('illust\/', link2).end():]
						})
			if results:
				final_results.append({
					'site': site,
					'thumbnail': thumbnail,
					'img_detail':{
						'width': width,
						'height': height,
						'type': img_type,
						'size': file_size
						}, 
					'results':results,
					'hash': hash_
					})
	return {'hash':hash_self, 'results': final_results}




