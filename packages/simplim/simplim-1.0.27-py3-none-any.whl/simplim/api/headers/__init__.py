r"""@2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

headers for many website
"""

module_path = __file__[:-11]

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'

referers = {
	'None': '',
	'pixiv': 'https://www.pixiv.net/',
	'dmzj': 'https://manhua.dmzj.com/',
	'baidu': 'https://www.baidu.com/',
	'bili': 'https://www.bilibili.com'
}


def get(site ,agent = agent):
	headers = {
		'user-agent': agent,
		'referer':  referers[site]
	}
	return headers

# header = {
#     "User-Agent": 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
# }
# 
# Baidu_grab = requests.get(url, headers=header)