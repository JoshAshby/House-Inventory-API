#!/usr/bin/env python2
'''
Basic image stuff using PIL

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
'''

import Image
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)


class PicError(Exception):
	'''
	class documentation
	PicError for use by the pic module
	'''
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class Pics(object):
	def __init__(self, barcode=''):
		self.barcode = barcode
		
	def Thumb(self):
		size = 128, 128
		
		try:
			monkey = open(abspath + '/pictures/thumb/' + self.barcode, 'wb')
		except:
			raise PicError('Can\'t open/make thumbnail file')
			
		try:
			baggins = Image.open(abspath + '/pictures/' + self.barcode)
			baggins.thumbnail(size)
			baggins.save(monkey)
		except:
			raise PicError('Can\'t open or process picture')
