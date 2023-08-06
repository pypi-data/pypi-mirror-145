from matplotlib import pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
import base64
import cv2
import os

module_path = os.path.join(os.path.dirname(__file__), '')

def raw2arr(raw, rgb=0):
	arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_ANYCOLOR)
	if rgb:
		b,g,r = cv2.split(arr)  
		arr = cv2.merge([r,g,b])
	return arr

def arr2raw(arr, rgb=0):
	if rgb:
		r,g,b,a = cv2.split(arr)  
		arr = cv2.merge([b,g,r])
	return cv2.imencode('.jpg', arr)[1].tobytes()


def raw2base64(raw):

	return base64.b64encode(raw).decode()

def any2raw(img, type_):
	if type_ == 'base64':
		return base64.b64decode(img)
	elif type_ == 'arr':
		return cv2.imencode('.jpg', img)[1].tobytes()
	elif type_ == 'plt':
		fig = plt.figure()
		cvs = fig.canvas
		cvs.print_png(img)

def gray4raw(raw):
	img_cv = raw2arr(raw)
	img_cv_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
	return arr2raw(img_cv_gray)

def resize(arr, size):
	pass

def avglight(array, amount):
	for row in array:
		for pixel in row:
			rate = np.max(pixel[:3]) / amount
			if rate:
				pixel[0]/=rate
				pixel[1]/=rate
				pixel[2]/=rate
			else:
				pixel[0]+=amount
				pixel[1]+=amount
				pixel[2]+=amount
	return array

def draw(path, text, pos=(0, 0), font = os.path.join("Fonts", "STXIHEI.ttf"), size = 18, color='#000000'):
	img = Image.open(path)
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype(font, size)
	draw.text(pos, text, font = font, fill = color)
	return img




