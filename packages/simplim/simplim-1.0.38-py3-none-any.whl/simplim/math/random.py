import numpy as np  
from time import time

def boxmuller():
	sigma = 1
	size = 1
	u = np.random.uniform(size=size)  
	v = np.random.uniform(size=size)  
	z = np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v)  
	return (z * sigma)[0]

class Mersenne:
	def __init__(self):
		self.index = 624
		self.MT = [0]*self.index
	def inter(self, t):
		return(0xFFFFFFFF & t) #取最后32位->t

	def twister(self):
		for i in range(624):
			y = self.inter((self.MT[i] & 0x80000000) +(self.MT[(i + 1) % 624] & 0x7fffffff))
			self.MT[i] = self.MT[(i + 397) % 624] ^ y >> 1
			if y % 2 != 0:
				self.MT[i] = self.MT[i] ^ 0x9908b0df
		self.index = 0

	def exnum(self):
		if self.index >= 624:
			self.twister()
		y = self.MT[self.index]
		y = y ^ y >> 11
		y = y ^ y << 7 & 2636928640
		y = y ^ y << 15 & 4022730752
		y = y ^ y >> 18
		self.index = self.index + 1
		return self.inter(y)

	def mainset(self,seed):
		self.MT[0] = seed	#seed
		for i in range(1,624):
			self.MT[i] = self.inter(1812433253 * (self.MT[i - 1] ^ self.MT[i - 1] >> 30) + i)
		return self.exnum()

	def twist(self,mi,ma):
		so = self.mainset(int(time())) / (2**32-1)
		rd = mi + int((ma-mi)*so)
		return rd
