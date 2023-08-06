import inspect, random, json, math, threading, inspect, ctypes
 
 
def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)

class empty:
	def __init__(self):
		pass
		

class list(list):
	"""docstring for list"""
	def __init__(self, arg = []):
		super(list, self).__init__(arg)
	def swap(self, a, b):
		x = self[a]
		self[a] = self[b]
		self[b] = x
		return self
	def shuffle(self, times = 100):
		for time in range(0, times):
			a = random.randint(0, self.length-1)
			b = random.randint(0, self.length-1)
			self.swap(a, b)
		return self
	def subscriptable(self, arg):
		if type(arg) == type([]) or type(arg) == type(list([])):
			return True
		return False
	def have(self, arg):
		for value in self:
			if arg == value:
				return True
			elif self.subscriptable(value):
				value = list(value)
				if value.have(arg):
					return True
		return False
	def isempty(self):
		if len(self) == 0:
			return True
		return False


class str(str):
	"""docstring for str"""
	def __init__(self, arg = ''):
		super(str, self).__init__()
	def reverse(self):
		index = -1
		ret = ''
		for char in self:
			ret += self[index]
			index -= 1
		self = ret
		return ret
	def belongto(self, symbols):
		if len(self) != 1:
			return False
		for symbol in symbols:
			if self == symbol:
				return True
		return False
	def isnumber(self):
		try:
			float(self)
		except:
			return False
		else:
			return True

class simdict(dict):
	def __init__(self, dict_, check = True):
		if type(dict_) == type(''):
			dict_ = json.load(open(dict_))
		super().__init__(dict_)
		self.__seed__ = 0
		if type(dict_) != type(dict()):
			print('failed to convert data to simdict')
			return
		try:
			for key in dict_:
				# print(key, dict_[key])
				if type(dict_[key]) == type(dict()):
					obj = simdict(dict_[key])
				else:
					obj = dict_[key]
				key = self.check(key)
				exec('self.'+key+' = obj')
		except Exception as e:
			raise e
			print('please make sure your json keys are legal variable')
		self.__vars__ = sorted(vars(self))[1:]
		self.dict_ = dict_
		# self.__varnum__ = len(self.__vars__)
	def check(self, key):
		try:
			exec(key+' = None')
		except:
			tmp = '_sd'+ str(self.__seed__)
			self.__seed__ += 1
			# print(key,'has been modified to',tmp)
			return tmp
		else:
			return key
	def get(self, key):
		if type(key) == int:
			key = self.__vars__[key]
			exec('self.ret = self.'+key)
			return self.ret
		elif type(key) == str:
			return self[key]
	def dump(self, path, indent = 4):
		open(path,'w').write(self.output(indent = indent))
	def output(self, indent = 4):
		return json.dumps(self, indent = indent)
	def __keys__(self):
		for key in self:
			print(key)
	# def __getitem__(self, key):
	# 	if type(self.dict_[key]) == str:
	# 		return self.dict_[key]
	# 	return simdict(self.dict_[key])


class Thread(threading.Thread):
	"""docstring for Thread"""
	def __init__(self, arg):
		super(Thread, self).__init__()
	def stop(self):
		thread.stop_thread(self)




		