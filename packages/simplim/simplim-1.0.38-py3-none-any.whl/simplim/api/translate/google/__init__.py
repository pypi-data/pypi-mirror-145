import requests
import json

host = 'http://translate.google.cn/translate_a/single'

headers = {
	'client':'gtx',
	'dt':'t',
	'ie':'UTF-8',
	'oe':'UTF-8',
	'sl':'auto',
	'tl':'zh-cn',
	'q':''
}

# 随便用，随便搞，能用多久不知晓
link = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&ie=UTF-8&oe=UTF-8'

# link2用多了会被淦（悲
link2 = 'http://translate.googleapis.com/translate_a/t?client=gtx&dt=t&ie=UTF-8&oe=UTF-8'

def get(q, tl='zh-cn', sl='auto', link = link):
	return requests.get(link+'&sl='+sl+'&tl='+tl+'&q='+q).json()

def translate(q, tl='zh-cn', sl='auto'):
	a_list = []
	a_str = ''
	for a in get(q,tl,sl)[0]:
		a_list.append(a[0])
		a_str += a[0]
	return a_list, a_str

def translate2(q, tl='zh-cn', sl='auto'):
	return get(q,tl,sl,link2)[0]

# 似乎没必要
# def translate_list(q_list, tl='zh-cn', sl='auto'):
# 	a_list = []
# 	for q in q_list:
# 		a_list.append(translate(q))
# 	return a_list