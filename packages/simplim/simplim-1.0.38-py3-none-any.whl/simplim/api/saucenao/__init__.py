r"""@2022 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool using website <https://saucenao.com/> to search & match anime pics
"""

import requests as rq
from bs4 import BeautifulSoup as bs

test_image = 'https://i.pximg.net/c/240x480/img-master/img/2022/02/24/00/00/10/96477280_p0_master1200.jpg'
search_url = 'https://saucenao.com/search.php?url='
user_url = 'https://saucenao.com/user.php'
host = 'https://saucenao.com'

header = {
	'origin': host,
	'referer': user_url,
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

global login_res
login_res = None

s = rq.Session()

def login():
	up = s.get(user_url,headers = header)
	token = bs(up.text,'lxml').find('input',{'name':'token'}).attrs['value']
	data = {
		'username': 'hardrelice',
		'password': 'h0a9r2d3relice',
		'token': token
	}
	header['token'] = token
	return s.post(url=f'{user_url}?page=login', headers=header, data=data)

def search_deprecate(url):
	global login_res
	if not login_res:
		login_res = login()
	res = s.get(search_url+url, headers=header)
	if res.status_code != 200:
		login()
		res = s.get(search_url+url, headers=header)
	page = bs(res.text,'lxml')
	results = page.find_all(class_ = 'resulttable')
	if len(results)==0:
		return -1
	package = []
	for result in results:
		similarity_str = result.find(class_='resultsimilarityinfo').text
		similarity = float(similarity_str[:-1])
		thumbnail = result.find(class_='resultimage').find('img').get('src')
		title = result.find(class_='resulttitle').text
		print(thumbnail)
		content = result.find(class_='resultcontentcolumn')
		site = 'None'
		if content.find('strong'):
			site = content.find('strong').text
		TV = 'None'
		ID = 'None'
		ID_link = 'None'
		author = 'None'
		author_link = 'None'
		if site=='None':
			pass
		elif site=='Title: ':
			site = 'None'
			TV = content.text
		else:
			site=site[:-5]
			info = content.find_all(class_='linkify')
			if len(info)!=0:
				try:
					ID = info[0].text
					ID_link = info[0].get('href')
				except:
					ID = ''
					ID_link = ''
				try:
					author = info[1].text
					author_link = info[1].get('href')
				except:
					author = ''
					author_link = ''
		pack={'similarity_str':similarity_str, 'similarity':similarity, 'thumbnail':thumbnail, 'title':title, 'site':site,'TV':TV, 'ID':ID, 'author':author, 'ID_link':ID_link, 'author_link':author_link}
		package.append(pack)
	return package

def search(url):
	global login_res
	if not login_res:
		login_res = login()
	res = s.get(f"{search_url}{url}", headers=header)
	if res.status_code != 200:
		login()
		res = s.get(search_url+url, headers=header)
	page = bs(res.text,'lxml')
	results = page.find_all(class_ = 'resulttable')
	if len(results)==0:
		return -1
	package = []
	for result in results:
		similarity_str = result.find(class_='resultsimilarityinfo').text
		similarity = float(similarity_str[:-1])
		thumbnail = result.find(class_='resultimage').find('img').get('src')
		if thumbnail == 'images/static/blocked.gif':
			thumbnail = result.find(class_='resultimage').find('img').get('data-src')
		title = result.find(class_='resulttitle').text
		print(thumbnail)
		rcc = result.find_all(class_='resultcontentcolumn')
		pack = {
			'similarity_str': similarity_str,
			'similarity': similarity,
			'title': title,
			'thumbnail': thumbnail,
			'info': []
		}
		tmp = ['',[]]
		for col in rcc:
			for c in col.children:
				if c.name == 'strong':
					if tmp[0]:
						pack['info'].append(tmp)
					tmp = [c.text,[]]
				else:
					if not c.text:
						pass
					elif c.name == 'a' and 'href' in c.attrs:
						tmp[1].append(f'{c.text} {c.attrs["href"]}')
					else:
						tmp[1].append(f'{c.text}')
		if tmp[0]:
			pack['info'].append(tmp)
		package.append(pack)
	return package