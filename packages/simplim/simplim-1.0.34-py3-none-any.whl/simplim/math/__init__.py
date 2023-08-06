from math import *

def C(a, b):
	if a < b or not type(a) == type(0) or not type(b) == type(0) or b < 1:
		return 0
	return int(A(a, b) / A(b, b))

def A(a, b):
	if a < b or not type(a) == type(0) or not type(b) == type(0) or b < 1:
		return 0
	num = 1
	for a in range(a - b + 1, a + 1):
		num *= a
	return num

def D(n):
	if not type(n) == type(0):
		return 0
	else:
		if n <= 1:
			return 0
		if n == 2:
			return 1
		if n == 3:
			return 2
		else:
			return (n - 1) * (D(n - 1) + D(n - 2))

def mod(value1, value2):
	pt1 = value1//value2
	pt2 = value1 % value2
	return pt1,pt2

def any2decimal(base, value):
	length = len(value)-1
	decimal = 0
	for val in value:
		decimal += val * base ** length
		length -= 1
	return decimal

def decimal2any(base, decimal):
	value = []
	pt1 = -1
	while pt1!=0:
		pt1, pt2 = mod(decimal, base)
		value.insert(0,pt2)
		decimal = pt1
	return value

def base_convert(from_base, to_base, value):
	return decimal2any(to_base, any2decimal(from_base, value))

def string2ascii(string, bias = 0):
	value = []
	for char in string:
		value.append(ord(char)+bias)
	return value

def ascii2string(value, bias = 0):
	string = ''
	for val in value:
		string += chr(val+bias)
	return string

def string_from_base_list(value, base):
	form = base_list[base]
	string = ''
	for val in value:
		string+=form[val]
	return string

def value_from_base_list(string, base):
	form = base_list[base]
	value = []
	for char in string:
		value.append(form.index(char))
	return value

base_list = {
				58:'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
				64:'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxy0123456789+/',
				91:'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxy0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'
			}

def encode_base(string, base, use_ascii=False, bias = 33):
	if base in base_list and not use_ascii:
		return string_from_base_list(base_convert(256, base, string2ascii(string)), base)
	else:
		return ascii2string(base_convert(256, base, string2ascii(string)), bias = bias)

def decode_base(string, base, use_ascii=False, bias = 33):
	if base in base_list and not use_ascii:
		return ascii2string(base_convert(base, 256, value_from_base_list(string,base)))
	else:
		return ascii2string(base_convert(base, 256, string2ascii(string, bias =- bias)))

def b58encode(tmp:str) -> str:
	tmp = list(map(ord,tmp))
	temp = tmp[0]
	base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	for i in range(len(tmp)-1):
		temp = temp * 256 + tmp[i+1]
	tmp = []
	while True:
		tmp.insert(0,temp % 58)
		temp = temp // 58
		if temp == 0:
			break
	temp = ""
	for i in tmp:
		temp += base58[i]
	return temp

def b58decode(tmp:str) -> str:
	import binascii
	base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	temp = []
	for i in tmp:
		temp.append(base58.index(i))
	tmp = temp[0]
	for i in range(len(temp)-1):
		tmp = tmp * 58 + temp[i+1]
	return binascii.unhexlify(hex(tmp)[2:].encode("utf-8")).decode("UTF-8")
