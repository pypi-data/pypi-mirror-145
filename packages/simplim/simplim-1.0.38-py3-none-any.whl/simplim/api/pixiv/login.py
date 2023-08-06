from bs4 import BeautifulSoup as bs
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
			'Host':'accounts.pixiv.net',
			'Referer':'https://accounts.pixiv.net/login',
			'Content-Type':'text/html; charset=UTF-8'
		}

headers2 = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
		'Host':'accounts.pixiv.net',
		'Referer':'https://accounts.pixiv.net/login',
		'Content-Type':'application/x-www-form-urlencoded'
}

# get提交参数
params ={
		'lang': 'en',
		'source': 'pc',
		'view_type': 'page',
		'ref': 'wwwtop_accounts_index'
		}

# post提交参数
datas = {
		'pixiv_id': '122527455@qq.com',
		'password': 'ldhllzLLZ-520',
		'captcha': '',
		'g_reaptcha_response': '',
		'post_key': '',
		'source': 'pc',
		'ref': 'wwwtop_accounts_indes',
		'return_to': 'https://www.pixiv.net'
		# 'reaptcha_enterprise_score_token':'03AGdBq25_End4u7euuSMRoIPN8CGb9Ds1Ued6Rm9syQawaIyV2tAJVZUw8HYOnbAjWMmqDhESEMZVt_dB1tmUL2kBwMH1hp2OnabHkeL7xmfQuxpaHUqVBxeIKO9TWQjSYIb2hefXVinUqGJ0yEbqX6kRvvtF4PKoxTocosd9P7LD1_GEv8ULYuQnBMPOTZM5N0lSXsEwU_Ay7OGTwzEbf41WsnS1fS_NXYepBZRzIY3JBJaw2PlKD7FtsYbwUeC6A_Up8AFcClJjMDUEbjWPPxnHEC01NYMGy0LgZeBThp7lOQubzN7-XuyD2LdYWLlk1373Ua2d9RU2LLrhsL57ZGcTFEgMmDI9QQc_ylcnDGaG-OxYJ_-5sftI7UAjpQEV52C2Uu67UybDsIxok8uhCcn3s7z0qva3apCDw0y-jHm7BnPhlCqCqaLhw324S-auWH1nd120e2DlaiXP-bNtX_LgAtQXFONgTExB9O9MHvcwDkiebYVrnkKdrTOz4xvvh5lAU5oWxei85cmO28ZRQI1Jo6JdjTlvVZRC_SfFGpZ1HsLt3oPYeJLqx14K4BjL1bk8T6xCV3H8kjLtxu8WOTUm1M6ZLkCeEpvAdUZLGwWotc5UkMx2E-0-MjdcvhCwR5FfaF65HT4YyMreOh2wIfuuy6-lRjNYSyAFrrsx12rZoxh_mar5a8DE06dutB7HENcSCVXS5Us8avUbXAClOobPzDP8EALu1ukbUAecc-yiUA90VglAys_NQsNCVNmnPSDQ-gtF3sZ9a_lEZkcuOXzEB1kWWeZgRMPErl5nKpebRldQ105sT273kQmIeHU9-zMPUGYHqQogfG5dvRHvd1vr1Glg2pRpvnuPC8fVx2OrbI__xKewlC9qdFZNkvJrFzWXRL45rGlTpeRY0_qpLPLuz183twezw5IJ-aTMygW-PXLYkJkW_LYNwGuUa48coXsbYAbYiXu0_xhkYmfmuhf_7rBOjs6hJENB5dWQuT4yXTgWpjUMG7i_xMIXN0TL1f1AMD3bgBORIa8WeWRNA_wWc9FIpDvfmGpqAJuEoJEt6U3fNCqsPwN-plSDC3bDmMswyyK60hL1v2wgm5eGgS9dd-Vlab3aRfTixO_G_F9rxfSqUg1uITCPHxZ-GUv02pIhIWv4SJjfi-V2LwDh3M0DV5JFeN3IlgdebXR4Mj_JCVqN9DuXdZgQUUYI-52X5PBueMNARVQzvDMBToWDd_540qHFBbB-44Ydmw_4_jUHXpCNfWOMPIGrOtW9m_x1KZuvKDVRWsEWBE4uoXfR5nbzd4eoSG3MibYscFkDyAAACXooYQDifHXfiyB7sBZ3PYLe8bbvR6IApLsHklC72lYc6bv5wWqYDmz6FrZUpSQexuZVuKkNqE27LuQOTjaj23SSy5OXznYEVpUoqfDD8008fxibYvmBKwj5ft-zcrbmP-VgrNjmz38MX3WbC1CKxG96I8dHorm7'
	}

login_url = 'https://210.140.131.206/login' # 登陆的URL
post_url = 'https://210.140.131.206/api/login?lang=en' # 提交POST请求的URL
analytics_url1 = 'https://www.google-analytics.com/j/collect?v=1&_v=j87&a=2064393434&t=pageview&_s=1&dl=https%3A%2F%2Faccounts.pixiv.net%2Flogin%3Freturn_to%3Dhttps%253A%252F%252Fwww.pixiv.net%252F%26lang%3Dzh%26source%3Dpc%26view_type%3Dpage&dr=https%3A%2F%2Fwww.pixiv.net%2F&ul=zh-cn&de=UTF-8&dt=%E7%99%BB%E5%BD%95%20%7C%20pixiv&sd=24-bit&sr=1440x900&vp=1440x737&je=0&fl=32.0%20r0&_utma=235335808.867814591.1612518455.1612607565.1612610035.4&_utmz=235335808.1612518455.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none)&_utmht=1612613208458&_u=AAECAEABAAAAAC~&jid=762514891&gjid=800111070&cid=867814591.1612518455&tid=UA-76252338-1&_gid=614123860.1612518483&_r=1&_slc=1&z=317754011'
analytics_url2 = 'https://www.google-analytics.com/j/collect?v=1&_v=j87&a=2064393434&t=pageview&_s=1&dl=https%3A%2F%2Faccounts.pixiv.net%2Flogin%3Freturn_to%3Dhttps%253A%252F%252Fwww.pixiv.net%252F%26lang%3Dzh%26source%3Dpc%26view_type%3Dpage&dr=https%3A%2F%2Fwww.pixiv.net%2F&ul=zh-cn&de=UTF-8&dt=%E7%99%BB%E5%BD%95%20%7C%20pixiv&sd=24-bit&sr=1440x900&vp=1440x737&je=0&fl=32.0%20r0&_utma=235335808.867814591.1612518455.1612607565.1612610035.4&_utmz=235335808.1612518455.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none)&_utmht=1612613208472&_u=QAECAEABAAAAAC~&jid=1985710891&gjid=307760021&cid=867814591.1612518455&tid=UA-76252338-4&_gid=614123860.1612518483&_r=1&gtm=2wg1r0KF8TRV&z=424454930'

s = requests.Session()

# 获取登录页面
res = s.get(login_url, headers = headers, verify=False)

parsed = bs(res.text,'lxml')
inp = parsed.find_all('input')
for i in inp:
	if i.get('name')=='post_key':
		post_key = i.get('value')
		break

print(res.text)

# 获取post_key
# pattern = re.compile(r'name="post_key" value="(.*?)">')
# r = pattern.findall(res.text)
# datas['post_key'] = r[0]
datas['post_key'] = post_key
# 模拟登录
result = s.post(post_url, headers = headers2, data = datas, verify=False)

# 打印出json信息
print(result.json())
