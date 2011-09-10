#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main admin functions

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import re
import time

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
import auth

urls = (
	'', 'slash',
	'/(.*)/', 'log'
)

class log:
	'''
	class documentation
	Generates the use log about the given product.
	'''		
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
			A JSON object like: 
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		try:
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		log = productDoc.get(bar)['log']
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"log": log})
	
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Returns:
		
		'''
		pass
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Returns:
		
		'''
		pass
	
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Returns:
		
		'''
		pass
	
	def GET(self, bar):
		return self.getFunc(barcode=bar)
	
	@auth.oauth_protect
	def POST(self, bar):
		return self.postFunc(barcode=bar)
	
	@auth.oauth_protect
	def PUT(self, bar):
		return self.putFunc(barcode=bar)
	
	@auth.oauth_protect
	def DELETE(self, bar):
		return self.deleteFunc(barcode=bar)
			

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()