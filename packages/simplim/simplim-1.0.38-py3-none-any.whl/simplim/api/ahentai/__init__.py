from bs4 import BeautifulSoup as bs
import requests as rq
import re, json, simplim, os
readOnline = 'https://ahentai.top/index.php?route=comic/readOnline&comic_id='
galleryPage = 'https://ahentai.top/index.php?route=comic/article&comic_id='
import urllib3
urllib3.disable_warnings()
def Download(id_, path=''):
	id_ = str(id_)
	text = rq.get(readOnline+id_).text
	lxml = bs(text, 'lxml')
	name=lxml.find(id="content").find(class_='d').text
	if not path:
		path = name
	if not os.path.exists(path):
		try:
			os.mkdir(path)
		except:
			print('Invalid path!')
			return
	open(os.path.join(path,'id'),'w').write(id_)
	scripts = lxml.find_all('script')
	Image_List = ''
	for script in scripts:
		if re.search('Image_List', script.text):
			Image_List = script.text
	print(Image_List)
	host = 'https:' + re.search('\"(.*?)\"', Image_List).group(0)
	pattern = re.compile(r'Image_List = \[(.*?)\]')
	Image_List = json.loads(pattern.search(Image_List).group(0)[13:])
	pics = len(Image_List)
	try:
		for Image in Image_List:
			url = host+Image['sort']+'.jpg'#Image['extension']
			if not os.path.exists(os.path.join(path,Image['sort']+'.'+'jpg')):
				simplim.curl(path, Image['sort']+'.'+'jpg' , url)
	except:
		return

def multiDownload(id_, path=''):
	id_ = str(id_)
	text = rq.get(readOnline+id_).text
	lxml = bs(text, 'lxml')
	name=lxml.find(id="content").find(class_='d').text
	if not path:
		path = name.replace('/',':')
	if not os.path.exists(path):
		try:
			os.mkdir(path)
		except:
			print('Invalid path!')
			return
	open(os.path.join(path,'id'),'w').write(id_)
	scripts = lxml.find_all('script')
	Image_List = ''
	for script in scripts:
		if re.search('Image_List', script.text):
			Image_List = script.text
	print(Image_List)
	host = 'https:' + re.search('\"(.*?)\"', Image_List).group(0)[1:-1]
	pattern = re.compile(r'Image_List = \[(.*?)\]')
	Image_List = json.loads(pattern.search(Image_List).group(0)[13:])
	pics = len(Image_List)
	try:
		for Image in Image_List:
			print(Image['sort'], '/', pics)
			url = host+Image['sort']+'.jpg'#Image['extension']
			if not os.path.exists(os.path.join(path,Image['sort']+'.'+'jpg')):
				simplim.multiThreadDownload(url = url, headers = {}, path = os.path.join(path, Image['sort']+'.'+'jpg'),verify=False,chunk_size=32)
	except Exception as e:
		raise e
		return

