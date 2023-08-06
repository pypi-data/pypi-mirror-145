r"""@2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool using api <https://v1.hitokoto.cn> to get sentence from hitokoto
api doc: <https://developer.hitokoto.cn/sentence/>
"""

import requests as rq

host = 'https://v1.hitokoto.cn/'

c_ = {
	'a': '动画',
	'b': '漫画',
	'c': '游戏',
	'd': '文学',
	'e': '原创',
	'f': '来自网络',
	'g': '其他',
	'h': '影视',
	'i': '诗词',
	'j': '网易云',
	'k': '哲学',
	'l': '抖机灵'
}

def call(c = '', encode = 'json', charset = '', callback = '', select = ''):
	params = {
		'c': c,
		'encode': encode,
		'charset': charset,
		'callback': callback,
		'select': select
	}
	response = rq.get(url = host, params = params).json()
	text = response['hitokoto']
	type_ = c_[response['type']]
	from_ = response['from']
	return text, type_, from_