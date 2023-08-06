import requests as rq
import simplim

url = 'http://fanyi.youdao.com/translate'
def translate(words='', doctype='json', type_='AUTO'):
	if not words:
		return 'None'
	words = simplim.filtemoji(words)
	params = {
		'doctype':doctype,
		'type': type_,
		'i': words
	}
	res = rq.get(url,params=params).json()
	if res['errorCode'] == 0:
		return res['translateResult'][0][0]['tgt']
	return -1

def translate_list(words='', doctype='json', type_='AUTO'):
	if not words:
		return 'None'
	results = []
	for word in words:
		results.append(translate(u''+simplim.filtemoji(word)))
	return results

# def get_params(words='', doctype='json', type_='AUTO'):
# 	params = {
# 		'doctype':doctype,
# 		'type': type_,
# 		'i': words
# 	}
# 	return params

# def get(params):
# 	return rq.get(url,params=params).json()


'''
{
	"returnPhrase": ["test"],
	"query": "test",
	"errorCode": "0",
	"l": "en2zh-CHS",
	"tSpeakUrl": "https://openapi.youdao.com/ttsapi?q=%E6%B5%8B%E8%AF%95&langType=zh-CHS&sign=C35E73F8BF03EB895783547A4115915F&salt=1648336282769&voice=4&format=mp3&appKey=2423360539ba5632&ttsVoiceStrict=false",
	"web": [{
		"value": ["测试", "测验", "试验", "考试"],
		"key": "Test"
	}, {
		"value": ["测试用例", "测试个案", "测试案例", "测试实例"],
		"key": "Test case"
	}, {
		"value": ["图灵测试", "杜林测试", "图林测试"],
		"key": "Turing test"
	}],
	"requestId": "6ed02748-329a-4ec3-8c1b-b3616887c555",
	"translation": ["测试"],
	"dict": {
		"url": "yddict://m.youdao.com/dict?le=eng&q=test"
	},
	"webdict": {
		"url": "http://mobile.youdao.com/dict?le=eng&q=test"
	},
	"basic": {
		"exam_type": ["初中", "高中", "CET4", "CET6", "考研"],
		"us-phonetic": "test",
		"phonetic": "test",
		"uk-phonetic": "test",
		"wfs": [{
			"wf": {
				"name": "复数",
				"value": "tests"
			}
		}, {
			"wf": {
				"name": "第三人称单数",
				"value": "tests"
			}
		}, {
			"wf": {
				"name": "现在分词",
				"value": "testing"
			}
		}, {
			"wf": {
				"name": "过去式",
				"value": "tested"
			}
		}, {
			"wf": {
				"name": "过去分词",
				"value": "tested"
			}
		}],
		"uk-speech": "https://openapi.youdao.com/ttsapi?q=test&langType=en&sign=50658FCD5391F844F6A8FE3F3A1A18CC&salt=1648336282769&voice=5&format=mp3&appKey=2423360539ba5632&ttsVoiceStrict=false",
		"explains": ["n. （书面或口头的）测验，考试；（医疗上的）检查，化验，检验；（对机器或武器等的）试验，检验；（对水、土壤、空气等的）检测，检验；（衡量能力或技能等的）测试，考验；医疗检查设备；化验结果；（常指板球、橄榄球的）国际锦标赛（Test）；准则，标准；（冶）烤钵，灰皿；（一些无脊椎动物和原生动物的）甲壳", "v. 试验，测试；测验，考查（熟练程度，知识）；检测，检验（质量或含量）；检查（身体），（用试剂）化验；考验；尝，（触）试"],
		"us-speech": "https://openapi.youdao.com/ttsapi?q=test&langType=en&sign=50658FCD5391F844F6A8FE3F3A1A18CC&salt=1648336282769&voice=6&format=mp3&appKey=2423360539ba5632&ttsVoiceStrict=false"
	},
	"isWord": true,
	"speakUrl": "https://openapi.youdao.com/ttsapi?q=test&langType=en&sign=50658FCD5391F844F6A8FE3F3A1A18CC&salt=1648336282769&voice=4&format=mp3&appKey=2423360539ba5632&ttsVoiceStrict=false"
}
'''
url2 = 'https://aidemo.youdao.com/trans'
def translate2(words='',From='Auto',to='Auto'):
	if not words:
		return 'None'
	try:
		headers = {
			'origin': 'https://ai.youdao.com',
			'referer': 'https://ai.youdao.com/',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
		}
		data = {
			'q': words,
			'from': From,
			'to': to
		}
		res = rq.post(url2,data=data,headers=headers).json()
		return res['translation'][0]
	except Exception as e:
		print(e)
		return 'None'


