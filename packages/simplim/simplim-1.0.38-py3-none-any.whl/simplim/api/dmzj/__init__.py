r"""@2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool made for downloading comics from dmzj.com
"""

from bs4 import BeautifulSoup as bs
import simplim.api.translate.youdao as yd
from selenium import webdriver
from pathlib import Path
import requests as rq
import pypinyin
import random
import json
import time
import simplim
import os

module_path = __file__[:-11]

testurl = 'https://images.dmzj.com/b/%E5%88%AB%E5%BD%93%E6%AC%A7%E5%B0%BC%E9%85%B1%E4%BA%86/%E7%AC%AC1%E8%AF%9D_1491547130/01.jpg'

host	= 'https://manhua.dmzj.com/'

referer = 'https://manhua.dmzj.com/'

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
	'referer': referer
}

class DMZJ:
	def __init__(self):		
		self.option = webdriver.ChromeOptions()
		self.option.add_argument("headless")
		self.driver = None
		self.quited = 1
	def load(self):
		if self.quited:
			self.driver = webdriver.Chrome(options = self.option)
			self.quited = 0
	def quit(self):
		if not self.quited:
			self.driver.quit()
			self.quited = 1

Dmzj = DMZJ()

def getIdByName(name, full = 0):
	id_ = ''
	for i in pypinyin.pinyin(name, style=pypinyin.NORMAL):
		if full:
			id_ += ''.join(i)[0]
		else:
			id_ += ''.join(i)
	return id_

def getImg(url, name = 0, path = './', type_ = 'jpg', useCurl = 0 ,ui = 0):
	url = 'https:'+url
	if not name:
		name_ = str(simplim.tuple2str(simplim.localtime(6)))
	else:
		name_ = str(name)
	path_ = os.path.join(path, simplim.standardfile(name_) + '.' + type_)
	if not Path(path).exists():
		os.mkdir(path)
		print('[N] mkdir successed')
	if useCurl:
		os.system('curl --header "referer: '+ referer +'" -o '+ path_ + ' ' + url)
	else:
		if ui:
			f = simplim.download(url, headers, ui)
		else:
			f = rq.get(url, headers=headers).content
		print('\n','[N]',str(name_) + '.' + type_, 'successfully downloaded')
		open(path_, 'ab').write(f)

def getInfo(url):
	# try:
	Dmzj.driver.get(url)
	page = bs(Dmzj.driver.page_source, 'lxml')
	div = page.find('div', class_='cartoon_online_border')
	ul = div.find_all('li')
	info = []
	for li in ul:
		dict_ = dict(name = li.text, url = li.find('a').get('href'))
		info.append(dict_)
	return info
	# except:
		# print('[E]','Failed to getInfo')

def getPicUrl(url):
	url = host + url + '#@page=1'
	try:
		Dmzj.driver.get(url)
		options = bs(Dmzj.driver.page_source, 'lxml').find_all('option')
		urls = []
		for option in options:
			urls.append(option.get('value'))
		return urls
	except:
		print('[E]','Failed to get urls')

def getComic(name, id_ = None, path = './', type_ = 'jpg', useCurl = 0 ,ui = 0, chapter = 0):
	Dmzj.load()
	path_ = os.path.join(path, name)
	if id_:
		url = host + id_
		if rq.get(url).status_code != 200:
			print('[N]','Comic Not Found')
			Dmzj.quit()
			return
	else:
		if rq.get(host + getIdByName(name, 0)).status_code == 200:
			url = host + getIdByName(name, 0)
		elif rq.get(host + getIdByName(name, 1)).status_code == 200:
			url = host + getIdByName(name, 1)
		else:
			print('[N]','Comic Not Found')
			Dmzj.quit()
			return
	if not os.path.exists(path_):
		os.mkdir(path_)
	info = getInfo(url)
	if not chapter:
		for inf in info:
			urls = getPicUrl(inf['url'])
			path__ = os.path.join(path_, inf['name'])
			page = 1
			for url in urls:
				getImg(url, name = page, path = path__, type_ = type_, useCurl = useCurl ,ui = ui)
				page += 1
	else:
		try:
			print('try')
			ans = input('>>>',info[int(chapter)]['name'],'y/n?')
			if ans == 'y':
				path__ = os.path.join(path_, inf['name'])
				page = 1
				for url in urls:
					getImg(url, name = page, path = path__, type_ = type_, useCurl = useCurl ,ui = ui)
			else:
				return
		except:
			print('except')
			try:
				for inf in info:
					if re.search(chapter, inf['name']):
						ans = input('>>>',inf['name'],'y/n?')
						if ans == 'y':
							path__ = os.path.join(path_, inf['name'])
							page = 1
							for url in urls:
								getImg(url, name = page, path = path__, type_ = type_, useCurl = useCurl ,ui = ui)
							break
						else:
							return
			except:
				print('[E]','chapter error')
	# finally:
	Dmzj.quit()

def quit():
	Dmzj.quit()

def load():
	Dmzj.load()







