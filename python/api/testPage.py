#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
A test sub app for messing around with new things and what not before I decide to use them or not.

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import math
'''
From: http://webpy.org/install and http://code.google.com/p/modwsgi/wiki/ApplicationIssues
This must be done to avoid the import errors which come up with having linear.py and config.py
'''
try:
	from configSub import *
except:
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
from configSub import *
import baseObject

baseObject.urlReset()


@baseObject.route('/(.*)/')
class test(baseObject.baseHTTPObject):
	'''
	Testing page object. Functions include full REST with OAuth protection on the POST PUT DELETE calls.
	Testing frameowrk for unittests included.
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode')
		
		pass


app = web.application(baseObject.urls, globals())
