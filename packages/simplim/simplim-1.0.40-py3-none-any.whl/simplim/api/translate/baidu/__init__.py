import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://fanyi.baidu.com/#{}/{}/'

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options = option)

def translate(q, tl='zh-en'):
	turl = url.format(tl.split('-')[0],tl.split('-')[1]) + q
	print(turl)
	driver.get(turl)
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'container'))
    )
	time.sleep(5)
	page = bs(driver.page_source,'lxml')
	results_bs = page.find_all(class_='ordinary-output target-output clearfix')
	results = []
	for result in results_bs:
		results.append(result.text.strip(' '))
	return results

def dictionary(q, tl='zh-en'):
	turl = url.format(tl.split('-')[0],tl.split('-')[1]) + q
	driver.get(turl)
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
	page = bs(driver.page_source, 'lxml')
	results_bs = page.find_all(class_='ordinary-output target-output clearfix')
	results = []
	for result in results_bs:
		results.append(result.text.strip(' '))
	# nav_list = {'简明释义':'', '英英释义':'' , '中中释义':'', '双语例句':'','柯林斯词典':''}
	nav_items = page.find_all(class_='nav-item')
	nav_list = dict()
	for text in nav_items:
		s = page.find(attrs={'data-nav-text':text.get('data-stat-add')})
		string = ''
		for tag in s.find_all(attrs={'none123123':''}):
			if tag.text:
				string+=tag.text+'\n'
		if s:
			nav_list[text.get('data-stat-add')]=string[:-1]
		# print(text,page.find(attrs={'data-nav-text':text}))
	print(nav_list)
	return nav_list




'keywords-title'

'''keywords-container
keywords-content
keywords-content-text-ellipsis
keywords-word/keywords-means'''

'dictionary-title'
'dictionary-comment'
'dictionary-output'
'dictionary-exchange'

'dictionary-tags'





