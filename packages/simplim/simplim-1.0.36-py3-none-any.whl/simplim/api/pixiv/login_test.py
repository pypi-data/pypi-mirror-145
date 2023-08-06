import requests
import time
import hashlib
md5 = hashlib.md5()
# 7fbc63b1c4e2af910d3466be857c9d25
# 1612610100
# 1612610200

ran = range(1612610000, 1612610227)
for x in ran:
	for y in range(0,9):
		for z in range(0,9):
			for m in range(0,9):
				for n in range(0,9):
					md5.update('{}.{}{}{}{}'.format(x,y,z,m,n).encode('utf-8'))
					if md5.hexdigest()=='7fbc63b1c4e2af910d3466be857c9d25':
						print(x,'.',y,z,m,n)
				# print(md5.hexdigest())

for x in ran:
	for y in range(0,9):
		md5.update('{}.{}'.format(x,y).encode('utf-8'))
		if md5.hexdigest()=='7fbc63b1c4e2af910d3466be857c9d25':
			print(x,'.',y)

for x in ran:
	md5.update('{}'.format(x).encode('utf-8'))
	if md5.hexdigest()=='7fbc63b1c4e2af910d3466be857c9d25':
		print(x)


def call():
	url = "https://{}/api/login".format('210.140.131.206')
	user_id = '37265945'
	timestamp = time.time()
	# print(time.time())
	md5.update(format(time.time(),'.1f').encode('utf-8'))
	post_key = md5.hexdigest()
	print("post_key",post_key)
	Cookies = """p_ab_id=4;
	p_ab_id_2=5;
	p_ab_d_id=1503173602;
	__utma=235335808.867814591.1612518455.1612518455.{};
	__utmb=235335808.2.10.{};
	__utmc=235335808; 
	__utmz=235335808.1612518455.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 
	__utmv=235335808.|2=login%20ever=no=1^3=plan=normal=1^5=gender=male=1^6=user_id=${}=1^9=p_ab_id=4=1^10=p_ab_id_2=5=1^11=lang=zh=1; 
	_ga=GA1.2.867814591.1612518455; 
	_gid=GA1.2.614123860.1612518483; 
	_ga=GA1.3.867814591.1612518455; 
	_gid=GA1.3.614123860.1. 612518483; 
	device_token=46308907811d508b5cd9b728c0c225be; 
	privacy_policy_agreement=2; 
	c_type=17; 
	a_type=0; 
	b_type=1; 
	__utmt=1; 
	PHPSESSID=mes21k640pi5pnrj9kdhj0u6c6oj0m8g""".format(format(timestamp,'.1f'),format(timestamp,'.0f'),user_id).replace('\n','')
	print(Cookies)
	headers = {
		"Host":"accounts.pixiv.net",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:82.0) Gecko/20100101 Firefox/82.0",
		"Accept":"application/json",
		"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
		"Accept-Encoding":"gzip, deflate, br",
		"Referer":"https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page",
		"Content-Type":"application/x-www-form-urlencoded",
		"Origin":"https://accounts.pixiv.net",
		"Content-Length":"1699",
		"Connection":"keep-alive"
		# "Cookies": Cookies
	}

	data = {
		"password":"ldhllzLLZ-520",
		"pixiv_id":"122527455%40qq.com",
		"post_key":post_key,# 4bbe71e493eb1ae14ae7efd8c2007a9b
		"source":"pc",
		"return_to":"https%3A%2F%2Fwww.pixiv.net%2F&"
	}
	print(time.time())
	x = requests.post(url, headers=headers, data=data, verify=False)
	print(time.time())
	print(x)
	print(x.text)


call()
