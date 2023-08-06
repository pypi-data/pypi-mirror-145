r"""©2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool simplified many useful functions
"""

from io import BytesIO
import requests as requests
import threading
import random
import shutil
import time
import sys
import os
import re

module_path = os.path.join(os.path.dirname(__file__), '')

class sim():
	def __init__(self):
		super(sim, self).__init__()
		self._running = os.path.dirname(sys.argv[0])

class DownloadBar():
	def __init__(self):
		self.total = 0
		self.left = 0
		self.percent = 0
		self.speed_Mb = 0
		self.speed_b = 0

class MultiThreadDownloader:
	"""docstring for MultiThreadDownloader"""
	def __init__(self, url, headers, segments, path):
		self.url = url
		self.headers = headers
		self.segments = segments
		if not os.path.exists(path):
			self.fp = open(path,'wb')
			self.fp.close()
		else:
			ans = input('>>> File exists, continue?[y/*]')
			if ans == 'y':
				self.fp = open(path,'wb')
				self.fp.close()
			else:
				return
		self.fp = open(path,'rb+')
		self.size = requests.head(url, headers = headers).headers['content-length']
		self.size = int(self.size)
		print(self.size)
	def setPos(self):
		spos = []
		fpos = []
		persize = int(self.size / self.segments)
		intsize = persize * self.segments  # 整除部分

		for i in range(0, intsize, persize):
			spos.append(i)
			fpos.append(i + persize - 1)
		if intsize < self.size:	 # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
			fpos[self.segments - 1] = self.size
		
		self.spos = spos
		self.fpos = fpos
		print(spos, '\n',fpos)
	def downloadFile(self, spos, fpos):
		print('down')
		try:
			headers = {}
			headers["Range"] = "bytes=%d-%d" % (spos, fpos)
			for key in self.headers:
				headers[key] = self.headers[key]
			res = requests.get(self.url, headers = headers)
			self.fp.seek(spos)
			self.fp.write(res.content)
		except Exception as e:
			print ("downloadFile error: ", e)
	def run(self):
		self.setPos()
		tmp = []

		start_time = time.time()	# 计时起始点，为了计算平均速度

		for i in range(0, self.segments):
			t = threading.Thread(target = self.downloadFile, args=(self.spos[i], self.fpos[i]))
			t.setDaemon(True)	   # 主进程结束时，线程也随之结束
			t.start()
			tmp.append(t)
		sleep(1)
		for i in tmp:
			i.join()				# 等待线程结束
		self.fp.close()

		finish_time = time.time()   # 计时终点，为了计算平均速度
		delta_time = finish_time-start_time
		speed = float(self.size)/( 1000.0*(finish_time-start_time))
		print ( "spend time: %0.2f s" % float(finish_time-start_time) )
		print ( "finished... average speed: %0.2f KB/s" % speed )
		return self.size, delta_time, speed

def multiThreadDownload(url, headers, path, chunk_size=32, verify=True):
	headers['keep-alive']='close'
	res = requests.head(url, headers = headers, verify=verify)
	trying_times=0
	while 1:
		try:
			trying_times+=1
			print(trying_times)
			if trying_times==5:
				return False
			size = int(res.headers["Content-Length"])
			break
		except:
			res = requests.get(url, headers = headers, stream=True, verify = verify)
			continue
	res = requests.head(url, headers = headers, verify=verify)
	print ( "total size: %d" % size )
	n=int(size/1024/chunk_size)
	if not n:
		n = 1
	spos = []
	fpos = []
	persize = int(size/n)
	intsize = persize * n  # 整除部分

	for i in range(0, intsize, persize):
		spos.append(i)
		fpos.append(i+persize-1)
	if intsize < size:	 # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
		fpos[n-1] = size
	print ( spos )
	print ( fpos )
	global cnt
	cnt = 0
	def downloadFile(url, spos, fpos, fp):
		global cnt
		while 1:
			try:
				header = {}
				header["Range"] = "bytes=%d-%d" % (spos, fpos)
				for key in headers:
					header[key] = headers[key]
				res = requests.get(url, headers = header, timeout=10,verify=verify)
				fp.seek(spos)
				fp.write(res.content)
				print(fpos)
				cnt+=1
				print(cnt,'/',n)
				return
			except Exception as e:
				# print ("downloadFile error: ", e)
				print(fpos,'retry')
				continue

	fp = open(path, "wb")
	fp.close()
	fp = open(path, "rb+")
	tmp = []

	start_time = time.time()	# 计时起始点，为了计算平均速度

	for i in range(0, n):
		t = threading.Thread(target = downloadFile, args=(url,  spos[i], fpos[i], fp))
		t.setDaemon(True)	   # 主进程结束时，线程也随之结束
		t.start()
		tmp.append(t)
	for i in tmp:
		i.join()
						# 等待线程结束
	fp.close()

	finish_time = time.time()   # 计时终点，为了计算平均速度

	speed = float(size)/( 1000.0*(finish_time-start_time))
	print ( "spend time: %0.2f s" % float(finish_time-start_time) )
	print ( "finished... average speed: %0.2f KB/s" % speed )
	return True


def logo():
	logo = '╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM\n┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸\n╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸'
	print(logo)

def LOGO():
	logo = '██╗  ██╗ █████╗ ███████╗██████╗ ███████╗███████╗██╗	 ██╗███████╗███████╗\n██║  ██║██╔══██╗██╔══██║██╔══██╗██╔══██║██╔════╝██║	 ██║██╔════╝██╔════╝\n███████║███████║███████║██║  ██║███████║███████╗██║	 ██║██║	 ███████╗\n██╔══██║██╔══██║██╔═██╔╝██║  ██║██╔═██╔╝██╔════╝██║	 ██║██║	 ██╔════╝\n██║  ██║██║  ██║██║  ██╗██████╔╝██║  ██╗███████╗███████╗██║███████╗███████╗\n╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝╚══════╝'
	print(logo)

def say(x,*arg):
	if len(arg)==0:
		print('>>>', x)
	else:
		string = ''
		for y in arg:
			string += str(y)+' '
		print('>>>', x, string)

def hear(x):

	return input('>>> '+x)

def clear():

	os.system('clear')

def curl(path, name ,url):
	os.system('curl -o '+os.path.join(path, name)+' '+url)

def download(url, headers = {}, delta_time = 1, chunk_size = 8, ratio = 1000, object_ = None, need_content_length = True):
	down = requests.get(url, stream = True, headers = headers)
	if not need_content_length:
		f=BytesIO()
		f.write(down.content)
		return f
	trying_times = 0
	while 1:
		print(trying_times)
		if trying_times > 10:
			return 0
		try:
			length = down.headers['content-length']
			print(trying_times)
			break
		except:
			trying_times += 1
			down = requests.get(url, stream = True, headers = headers)
	print(down.headers)
	length = float(length)
	Kb = length / ratio
	Mb = Kb / ratio
	Mb_str = '{:.2f}'.format(Mb)
	done = 0
	done_pre = 0
	time_pre = time.time()
	f = BytesIO()
	for chunk in down.iter_content(chunk_size = chunk_size):
		if chunk:
			f.write(chunk)
			f.flush()
			done += len(chunk)
			if time.time() - time_pre > delta_time:
				percent = done / length * 100
				num = int(percent / 2)
				speed_b = (done - done_pre)/delta_time
				speed_Mb = (done - done_pre) / ratio / ratio / delta_time
				done_pre = done
				left = str(int((length - done)/speed_b))
				if object_:
					object_.percent = percent
					object_.total = Mb
					object_.speed_Mb = speed_Mb
					object_.speed_b = speed_b
					object_.left = left
				print('\r' + num*'█' + (50-num)*' ' + '{:.2f}'.format(percent) + '% ' + str(speed_Mb)[:4] + 'M/s ' + Mb_str +'M ' + left + 's   ',end='',flush=True)
				time_pre = time.time()
	# print('\n[N]', 'successfully downloaded')
	return f

def match(arg, arr):
	'''
	match(arg, arr) -> bool
	'''
	for opt in arr:
		if arg == opt[0]:
			return True
	return False

def findict_0(dict_, arr):
	'''
	dict={'1':{'2':{'3':'got it!'}}}
	dict=findict(dict,['1','2','3']) -> dict: 'got it!'
	'''
	if len(arr) != 0:
		dict_ = dict_[arr[0]]
		arr = arr[1:]
		dict_ =  findict(dict_,arr)
		return dict_
	else:
		return dict_

def findict(dict_, arr):
	if len(arr) != 0:
		if type(dict_) == type({'1':'1'}) :
			for key in dict_:
				if key == arr[0]:
					dict_ = dict_[arr[0]]
					arr  = arr[1:]
					dict_ = findict(dict_,arr)
					return dict_
			return 'Keyword not found!'
		else:
			return 'Keyword not found!'
	else:
		return dict_

def filtemoji(desstr, restr=''):
	try:
		co = re.compile(u'[\U00010000-\U0010ffff]')
	except re.error:
		co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
	return co.sub(restr, desstr)


def getcmd(cmd):
	which = -1
	cmdarr = []
	for char in range(len(cmd)):
		if cmd[char] != ' ' and char == 0:
			which+=1
			cmdarr.append('')
		if cmd[char] != ' ':
			cmdarr[which]+=cmd[char]
		if char == len(cmd)-1:
			break
		if cmd[char] == ' ' and cmd[char+1] != ' ':
			which+=1
			cmdarr.append('')
	if which == -1:
		return []
	return cmdarr

def parsedict(dict_):
	keys = []
	values = []
	for key in dict_:
		if type(dict_[key]) == type(dict_):
			keys.append(key)
		else:
			values.append(key)
	return keys, values

def checkdoc(list_, doc):
	for dir_ in list_:
		if dir_==doc:
			return 1
	return 0

def localtime(setting = 0):
	lt = time.localtime()
	if not setting:
		return lt
	else:
		return lt[:setting]

def tuple2str(tups, isPure = 1):
	string=''
	if isPure:
		for tup in tups:
			string+=str(tup)
		return string
	else:
		pre = str(tups)
		for p in pre:
			if p != '\'':
				string += p
		return string

def list2str(list_, spliter = ''):
	string = ''
	for item in list_:
		string += str(item) + spliter
	if spliter:
		return string[:-len(spliter)]
	return string

def listsum(*list_):
	List = []
	length = 0
	for sublist in list_:
		if len(sublist) > length:
			length = len(sublist)
	for ele in range(length):
		List.append(0)
	for x in range(length):
		for sublist in list_:
			if len(sublist) > x:
				List[x] += sublist[x]
	return List

def standardfile(file):
	sfile = ''
	for f in file:
		if f == '/':
			sfile += ':'
		elif f == ':':
			sfile += '：'
		else:
			sfile += f
	return sfile

def standardnum(num, length=2):
	l = len(str(num)) 
	if l < length:
		return '0' * (length - l) + str(num)
	else:
		return str(num)

def gettemp(setting=6):
	lt = localtime(setting)
	# print(lt)
	new_lt = []
	for t in lt:
		new_lt.append(standardnum(t,2))
	# print(new_lt)
	return list2str(new_lt)

def getargs(function):

	return function.__code__.co_varnames[:function.__code__.co_argcount]

def getargsnum(function):

	return function.__code__.co_argcount

def getargsdefault(function):
	
	return function.__defaults__

def classify(dict_, depth = 0, arr = [], key = 0):
	keys, values = parsedict(dict_)
	arr.append((depth, keys, values))
	if keys:
		depth += 1
		for key in keys:
			newdict_ = dict_[key]
			classify(newdict_, depth, arr, key)
	return arr

def classify2(dict_, depth = 0, key = 'main', type_ = 1, path = [], note = []):
	keys, values = parsedict(dict_)
	#path.append((depth, keys, values))
	note.append((depth, key, type_))
	if keys:
		depth += 1
		for key in keys:
			newdict_ = dict_[key]
			classify2(newdict_, depth, key, 1, path)
	if values:
		if not keys:
			depth += 1
		for value in values:
			note.append((depth, value, 0))
	return note

def addself(tab, key, value):
	if type(value) == type(''):
		return tab*'\t' + 'self.' + key + ' = \'\'\'' + value + '\'\'\'\n'
	else:
		return tab*'\t' + 'self.' + key + ' = ' + str(value) + '\n'

def deffunc(tab, name, args, funcarr):
	string = tab * '\t' + 'def ' + name + tuple2str(args, isPure = 0) + ':\n'
	for func in funcarr:
		try:
			intab = func[1]
		except:
			intab = 0
		try:
			cmd = func[0]
		except:
			cmd = func
		string += (tab + 1 + intab) * '\t' + cmd + '\n'
	return string

def easyclassify_arr(dict_, arr = []):
	keys, values = parsedict(dict_)
	if keys:
		for key in keys:
			newdict_ = dict_[key]
			easyclassify_arr(newdict_)
	if values:
		for value in values:
			arr.append((value,dict_[value]))
	return arr

def easyclassify(dict_):
	string = 'class Classify:\n\tdef __init__(self):\n'
	arr = easyclassify_arr(dict_)
	for a in arr:
		string += addself(2, a[0], a[1])
	try:
		os.mkdir('classify_temp')
		fp = open('classify_temp/__init__.py','w')
		fp.write(string)
		fp.close()
		import classify_temp
		shutil.rmtree('classify_temp')
		return classify_temp.Classify()
	except Exception as e:
		print('[E]','Failed to classify')
		raise e
#depth, key, type_ 0:value, 1:dict_

def rhash(value):
	if type(value) == type(''):
		length = len(value)
		tot = 0
		HashMap = ''
		Hash = ''
		pos = 0
		for var in value:
			h = hex(int(oct(int(bin((ord(var) + length)**3)[2:]))[2:]))[2:]
			tot += ord(var)
			HashMap += h
		avg = int(tot/length)
		size = len(HashMap)
		if size < 16:
			HashMap += (16-size) * 'k'
			size = 16
		# print('Map',HashMap)
		newHash = ''
		for i in range(0,16):
			num = 0
			for j in range(0,int(size/16)):
				num += ord(HashMap[j*16+i])
			newHash += chr(int(num*16/size))
		bias = tot % 27 + avg % 11
		for H in newHash:
			if pos%2 == 0:
				char = ord(H)+bias
				if char>=127 and char<=160:
					char += 34
				Hash += chr(char)
			pos += 1
		# print('Hash',Hash)
		return Hash
	if type(value) == type(0) or type(0.1):
		return value












































