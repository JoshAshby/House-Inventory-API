#!/usr/bin/env python
import Image

'''
Basic image stuff using PIL

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
'''

import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

def odinsThumb(barcode):
	size = 128, 128

	monkey = open(abspath + '/pictures/thumb/' + barcode + '_thumb.png', 'wb')

	baggins = Image.open(abspath + '/pictures/' + barcode + '.png', 'rb')
	baggins.thumbnail(size)
	baggins.save(monkey)