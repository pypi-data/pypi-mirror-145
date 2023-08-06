import requests, _thread, subprocess
import json,simplim,math,os
from bs4 import BeautifulSoup as bs
from simplim.premium import *
from simplim.api import pixiv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

myId = 37265945
# cookies may need update
myCookies = '''first_visit_datetime_pc=2020-11-28+21%3A45%3A00; p_ab_id=0; p_ab_pid2=8; p_ab_d_id=768000479; yupidb=Y5iFiTA; __utmc=235335808; __utmz=235335808.1606567577.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1655807374.1606567577; _gid=GA1.2.1942395672.1606567720; PHPSESSID=37265945_VkGbYQsEAz1HmDEedckZwLGs741E7Gc4; device_token=e6b006ff3061bcfb9209f43eb9b46a58; c_type=17; privacy_policy_agreement=2; a_type=0; b_type=1; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=37265945=1^9=p_ab_id=0=1^10=p_ab_pid2=8=1^11=lang=zh=1; ki_r=; ki_s=211476%3A0.0.0.0.0; tag_view_ranking=3mvlXxwzlR~Lt-oEicbBr~kW3BiTEuM5~5oPIfUbtd6~gaE4PqlBWi~W78rK-PX_4~oBBiJ9E6tU~JFhw3JD6Sk~Ie2c51_4Sp~-7RnTas_L3~-StjcwdYwv~jk9IzfjZ6n~cIvr1j-nV5~-98s6o2-Rp~EZQqoW9r8g~_EOd7bsGyl~azESOjmQSV~OCvRKdT9WZ~_hSAdpN9rx~rfT_nXpCc3~XDEWeW9f9i~ea63_dbx7n~qBkdYfMJCJ~vPCcmvyD83~yosAmL0cOs~LVSDGaCAdn~GIhj0ISHA-~sYhl4SsLi1~qWFESUmfEs~yTkpyMW416~c15D8Cg2xk~_3oeEue7S7~kW8varCrdB~g_eyEX5F12~IcyY_7-nC2~YUsR08CHCr~LJo91uBPz4~gSU99FHHmC~BR3w49OBEd~2RR-Wztsl7~PvCsalAgmW~E8zdna9OwN~pMSprni69U~BRqZEd57W7~7mUuJlWo2q~0xsDLqCEW6~9aCtrIRNdF~sUsFryn8PD~tjqOJfFjRQ~F7zpudQrCZ~rKTxHKO10-~ehFkU8vOq9~liM64qjhwQ~gB7nxsLSGV~Z-FJ6AMFu8~8lIIS3xJNi~IOEPYP3pVd~qGUmGYz8G0~cdv3zObps0~SzJt_scmqK~7XHbZ90olh~mUFTwA-J1U~f2T5iWzjIl~aVBy69AYIA~zc4NFUyEsx~FnKocX8sjN~MGdDsHJvI0~laabH-Abve~wDFsURnp8f~hMU3QbbDfI~6nciQgCSzR~vSWEvTeZc6~x8KjmDIT9c~E9anU9DdS_~lH5YZxnbfC~CdwexeFTM2~iUx3FpZLw5~uGQeWvelyQ~yIzBRqk7IT~kjfJ5uXq4m~O0RTa3uxaa~bvp7fCUKNH~GACl-vLazK~iszjNkquhZ~2R7RYffVfj~KN7uxuR89w~YCJduqB2Ci~SJ5KfO2OAx~gyXGHTTt7f~QaiOjmwQnI~D0nMcn6oGk~aPdvNeJ_XM~JN2fNJ_Ue2~CrFcrMFJzz~YjR-YYfhXC~sylWziJEvL~KOnmT1ndWG; __utma=235335808.1655807374.1606567577.1606641026.1606659126.6; __utmt=1; __utmb=235335808.1.10.1606659126; ki_t=1606568775267%3B1606618808129%3B1606659240848%3B2%3B38'''
myCookies = '''first_visit_datetime_pc=2021-02-04+11%3A45%3A36; p_ab_id=3; p_ab_id_2=3; p_ab_d_id=791773885; yuid_b=Igdlg2Q; __utmc=235335808; __utmz=235335808.1612406815.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.782120525.1612406815; device_token=b20582c81bf82826939b61fbe98f3af5; c_type=17; a_type=0; b_type=1; __utmv=235335808.|2=login%20ever=no=1^3=plan=normal=1^5=gender=male=1^6=user_id=37265945=1^9=p_ab_id=3=1^10=p_ab_id_2=3=1^11=lang=zh=1; ki_r=; ki_s=; __cfduid=dfbced14551f7863c218df14f0153c3cc1612411092; PHPSESSID=37265945_XudJtlKjIdC5HPKcIv36puNjuizPJB9i; privacy_policy_agreement=2; __utma=235335808.782120525.1612406815.1612505360.1612517083.4; __utmt=1; ki_t=1612406870043%3B1612505411837%3B1612517094783%3B2%3B6; __utmb=235335808.2.10.1612517083'''
myCookies = '''first_visit_datetime_pc=2021-02-05+18%3A46%3A23; p_ab_id=4; p_ab_id_2=5; p_ab_d_id=1503173602; yuid_b=J1YidXU; __utma=235335808.867814591.1612518455.1612833089.1615349265.9; __utmz=235335808.1612518455.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=no=1^3=plan=normal=1^5=gender=male=1^6=user_id=37265945=1^9=p_ab_id=4=1^10=p_ab_id_2=5=1^11=lang=zh=1; _ga=GA1.2.867814591.1612518455; privacy_policy_agreement=2; c_type=17; a_type=0; b_type=1; ki_t=1612518542450%3B1615349335933%3B1615349335933%3B4%3B12; ki_r=; PHPSESSID=37265945_AmF8pSxYnK1A1ypiGrEuALHPcI1m7zLM; __utmb=235335808.2.10.1615349265; __utmc=235335808; __utmt=1; _gid=GA1.2.924207260.1615349285; _gat=1; device_token=956473bc36a02da7d0fe357290e0a16f'''
# host = '210.140.131.203'
# pximg_host = '210.140.92.138'
try:
	host = socket.gethostbyname('pixiv.com')
except:
	host = '210.140.92.186'
try:
	pximg_host = socket.gethostbyname('pximg.net')
except:
	pximg_host = '210.140.92.143'
test_url='https://'+host+'/artworks/79025298?format=json'
headers = pixiv.headers

def getIllustInfo(pid):
	response = requests.get('https://'+host+'/artworks/'+str(pid), headers={'Host':'www.pixiv.net'},verify=False)
	if response.status_code != 200:
		return
	text = response.text
	soup = bs(text,'lxml')
	#open('h.html','w').write(text)
	content = soup.find('meta',id='meta-preload-data').get('content')
	dict_ = json.loads(content)
	dict_ = simdict(dict_)
	dict_.illust = simdict(dict_.illust[str(pid)])
	dict_.__dict__['manga_urls'] = []
	if dict_.illust.pageCount > 1:
		dict_.__dict__['manga']=True
		for page in range(0, dict_.illust.pageCount):
			s = dict()
			for url in dict_.illust.urls:
				s[url] = dict_.illust.urls[url].replace('p0','p'+str(page))
			dict_.__dict__['manga_urls'].append(s)
	else:
		dict_.__dict__['manga']=False
	return dict_

def getIllustInfoCompatible(pid):
	info = getIllustInfo(pid)
	processed = empty()
	if not info:
		return
	illust = info.illust
	for uid in info.user:
		user = info.user[uid]
	extra = illust.extraData.meta
	processed.info		= info
	processed.title		= illust.illustTitle
	processed.caption	= illust.illustComment
	processed.tags		= [ tag['tag'] for tag in illust.tags.tags ]
	processed.urls		= illust.urls
	processed.mini		= illust.urls.mini
	processed.thumb		= illust.urls.thumb
	processed.small		= illust.urls.small
	processed.regular	= illust.urls.regular
	processed.original	= illust.urls.original
	processed.width		= illust.width
	processed.height	= illust.height
	processed.createDate= illust.createDate
	processed.uploadDate= illust.uploadDate
	processed.age_limit	= illust.xRestrict
	processed.user		= user
	processed.pid		= illust.illustId
	processed.is_manga	= illust.pageCount != 1
	processed.manga		= []
	if processed.is_manga:
		pages	= range(1,illust.pageCount+1)
		for page in pages:
			processed.manga.append(processed.original.replace('p0','p'+str(page)))
	return simdict(processed.__dict__)

def getIllustUrls(pid):
	info = getIllustInfo(pid)
	if not info:
		return
	return info.illust.urls, info.manga_urls, info

def getIllust(pid, path='', use_curl=True, setting='original'):
	info = getIllustInfo(pid)
	if not info:
		return
	title= info.illust.title
	urls, manga_urls = info.illust.urls, info.manga_urls

	if manga_urls:
		print(manga_urls)
		if not path:
			path = title
		if not os.path.exists(path):
			os.mkdir(path)
		cnt=0
		for manga_url in manga_urls:
			ret = simplim.multiThreadDownload(url=manga_url[setting].replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=os.path.join(path,str(cnt)+'.jpg'),verify=False)
			if not ret:
				# d=simplim.download(url=manga_url[setting],headers=pixiv.headers,need_content_length)
				# open(os.path.join(path,str(cnt)+'.jpg'),'wb').write(d.getvalue()).close()
				pixiv.getImg(url=manga_url[setting].replace('i.pximg.net',pximg_host),name=str(cnt),path=path,useCurl=use_curl)
			cnt+=1
	else:
		print(urls)
		if not path:
			path = './'
		ret = simplim.multiThreadDownload(url=urls[setting].replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=os.path.join(path,title+'.jpg'),verify=False)
		if not ret:
			pixiv.getImg(url=urls[setting].replace('i.pximg.net',pximg_host), name=title,path=path,useCurl=use_curl)

def getIllustByUrl(url,path='',use_curl=False):
	# pixiv.getImg(url = url.replace('i.pximg.net',pximg_host),name=simplim.gettemp(),path=path,useCurl=use_curl)
	if use_curl:
		open(path,'wb').write(requests.get(url.replace('i.pximg.net',pximg_host), headers=headers, verify=False).content)
	else:
		simplim.multiThreadDownload(url=url.replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=path,verify=False)

def getUserLikedWorks(pid,use_curl = False):
	headers = {
		'host':'www.pixiv.net',
		'cookie': myCookies
	}
	params = {
		'tag':'',
		'offset': '0',
		'limit': '100',
		'rest':'show',
		'lang':'zh'
	}
	# ?tag=&offset=0&limit=48&rest=show&lang=zh
	response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False)
	if response.status_code == 200:
		if response.json()['error']:
			return
	else:
		return
	print(response.json())
	sd = simdict(response.json())
	total = sd.body.total
	works = sd.body.works
	limit = int(params['limit'])
	pages = total/limit
	print('\n\n\n'+str(total)+'\n\n\n')
	if pages>1:
		pages = range(0,int(pages))
		offset = 0
		for page in pages:
			offset += limit
			params['offset']=str(offset)
			while 1:
				try:
					response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False,timeout=10)
					break
				except:
					print('agian')
			sd = simdict(response.json())
			works += sd.body.works
		final = simdict({'works': works})
		final.dump('liked_works.'+str(pid)+'.'+simplim.gettemp()+'.json')
		return final
		# params['limit']=str(total)
		# response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False)
		# sd = simdict(response.json())
		# sd.dump(str(pid)+'.'+simplim.gettemp()+'.json')
	sd.body.works.dump(str(pid)+'.'+simplim.gettemp()+'.json')
	return sd

def getMainPage(cookie=myCookies):
	headers = {
		'host':'www.pixiv.net',
		'referer':'https://www.pixiv.net',
		'cookie': cookie
	}
	url = 'https://'+host+'/ajax/top/illust?mode=all&lang=zh'
	response=requests.get(url, headers = headers, verify=False)
	print(response.status_code)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getUserFollowingUsers(pid):
	headers = {
		'host':'www.pixiv.net',
		'cookie': myCookies,
		'tag':'',
		'offset':'0',
		'limit':'24',
		'rest':'show',
		'lang':'zh'
	}
	# ?offset=0&limit=24&rest=show&tag=&lang=zh
	response=requests.get('https://'+host+'/ajax/user/'+str(pid)+'/following', headers = headers, verify=False)
	text = response.json()
	sd = simdict(text)
	total = sd.body.total
	users = sd.body.users
	limit = headers['limit']
	pages = total/limit
	#open('h.html','w').write(text)
	# content = soup.find('meta',id='meta-preload-data').get('content')
	# dict_ = json.loads(content)
	# dict_ = simdict(dict_)
	return soup

def getRank(mode='daily', page=1):
	# if not date:
	# 	date = int(simplim.gettemp(3))-1
	url = 'https://'+host+'/ranking.php'
	params = {
		'mode': mode,
		'p': str(page),
		'format': 'json'
	}
	# if mode=='daily':
	# 	params['date'] = str(date)
	response = requests.get(url, params=params, headers={'Host':'www.pixiv.net'}, verify=False)
	if response.status_code == 200:
		if 'error' not in response.json():
			return response.json()

def getIllustRecommend(pid, limit=18):
	url = 'https://'+host+'/ajax/illust/'+str(pid)+'/recommend/init?limit='+str(limit)+'&lang=zh'
	response = requests.get(url, headers={'Host':'www.pixiv.net', 'cookie':myCookies, 'referer':'https://www.pixiv.net/artworks/'+str(pid)}, verify=False)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getMuiltiIllustsThumb(ids):
	url='https://'+host+'/ajax/illust/recommend/illusts'
	illust_ids = []
	for pid in ids:
		illust_ids.append('illust_ids%5B%5D='+str(pid))
	print('&'.join(illust_ids))
	url+='?'+'&'.join(illust_ids)+'&lang=zh'
	response = requests.get(url, headers={'Host':'www.pixiv.net'}, verify=False)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getLatestIllusts(page=1):
	url='https://'+host+'/bookmark_new_illust.php'
	params = {
		'p': page
	}
	response = requests.get(url,params=params, headers={'Host':'www.pixiv.net', 'cookie':myCookies}, verify=False)
	if response.status_code == 200:
		idname = 'js-mount-point-latest-following'
		text = response.text
		lxml = bs(text.replace('&quot;','\''),'lxml')
		data = lxml.find(id=idname).get('data-items')
		return json.loads(data.replace('\'','\"'))




def search(word,s_type='artworks',order='date_d',mode='all',p=1,s_mode='s_tag',type_='all',lang='zh',wlt=0,hlt=0):
	'''
		word: #url need to replace ' ' to %20
			mainWord -doninclude -anotherDoninclude (include OR anotherInclude)
			
			特殊词汇/标签
			オリジナル 原创
			10000users入り 10000以上收藏
			オリジナル10000users入り 原创10000以上收藏
			# 可以直接做成收藏筛选
			# 也可以做成搜索小提示
		s_type:
			artworks: 所有
			manga: 漫画
				type: manga
			illustrations: 插画，动图（继续用type定义）
				type: illust
					  ugoira
					  illust_and_ugoira

		order:
			date 正序
			date_d/任意 倒序
		mode:
			
		s_mode:
			s_tag
			s_tag_full
			s_tc

		ratio:
			0 正方形
			0.5 横
			-0.5 纵

		wlt: width 最小限制
		hlt: height 最小限制
		wgt: 最大
		hgt: 最大
		tool: 工具
			所有的制图工具
			SAI
			Photoshop
			CLIP STUDIO PAINT
			IllustStudio
			ComicStudio
			Pixia
			AzPainter4
			Painter
			Illustrator
			GIMP
			FireAlpaca
			網上描繪
			AzPainter
			CGillust
			描繪聊天室
			手畫博克
			MS_Paint
			PictBear
			openCanvas
			PaintShopPro
			EDGE
			drawr
			COMICWORKS
			AzDrawing
			SketchBookPro
			PhotoStudio
			Paintgraphic
			MediBang Paint
			NekoPaint
			Inkscape
			ArtRage
			AzDrawing4
			Fireworks
			ibisPaint
			AfterEffects
			mdiapp
			GraphicsGale
			Krita
			kokuban.in
			RETAS STUDIO
			emote
			4thPaint
			ComiLabo
			pixiv Sketch
			Pixelmator
			Procreate
			Expression
			PicturePublisher
			Processing
			Live2D
			dotpict
			Aseprite
			Poser
			Metasequoia
			Blender
			Shade
			3dsMax
			DAZ Studio
			ZBrush
			Comi Po!
			Maya
			Lightwave3D
			六角大王
			Vue
			SketchUp
			CINEMA4D
			XSI
			CARRARA
			Bryce
			STRATA
			Sculptris
			modo
			AnimationMaster
			VistaPro
			Sunny3D
			3D-Coat
			Paint 3D
			VRoid Studio
			筆芯筆
			鉛筆
			原子筆
			毫筆
			顏色鉛筆
			Copic麥克筆
			沾水筆
			透明水彩
			毛筆
			毛筆
			記號筆
			麥克筆
			水溶性彩色铅笔
			涂料
			丙烯顏料
			鋼筆
			粉彩
			噴筆
			顏色墨水
			蠟筆
			油彩
			COUPY-PENCIL
			顏彩
			蠟筆

		scd=2021-02-04 #开始时间 
		ecd=2021-03-05 #结束时间




	'''
	url ='https://'+host+'/ajax/search/'+s_type+'/'+word
	params = {
		'word':word,
		'order':order,
		'mode':mode,
		'p':p,
		's_mode':s_mode,
		'type':type_,
		'lang':lang
	}
	response = requests.get(url, params=params, headers={'Host':'www.pixiv.net'},verify=False)
	return response

# m = getUserLikedWorks(myId)
# m = getUserFollowingUsers(myId)

# z=requests.get('https://210.140.131.203/ajax/user/37265945/illusts/bookmarks?offset=0&limit=24&rest=show&tag=金的&lang=zh', headers={'host':'www.pixiv.net','cookie':myCookies}, verify=False)

# x=getUserLikedWorks(myId,0)
# print(len(x.works))
