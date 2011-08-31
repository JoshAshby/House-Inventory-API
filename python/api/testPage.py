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
	"", "slash",
	"/", "test"
)

class slash:
	def GET(self): raise web.seeother("/")

class test:
	'''
	class documentation
	
	Testing page object. Functions include full REST with OAuth protection on the POST PUT DELETE calls.
	Testing frameowrk for unittests included.
	'''
	def getFunc(self, *args):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		if debug: name = args[0]
		else:
			wi = web.input()
			name = wi['barcode']
		
		reply = {
			"barcode": name
		}
		
		answer = json.dumps(reply)
		
		return answer
	
	def postFunc(self, *args):
		'''
		function documentation
		
		POST verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(args[0])
	
	def putFunc(self, *args):
		'''
		function documentation
		
		PUT verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(args[0])
	
	def deleteFunc(self, *args):
		'''
		function documentation
		
		DELETE verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(args[0])
	
	def GET(self):
		return self.getFunc()
	
	@auth.oauth_protect
	def POST(self):
		return self.postFunc()
	
	@auth.oauth_protect
	def PUT(self):
		return self.putFunc()
	
	@auth.oauth_protect
	def DELETE(self):
		return self.deleteFunc()
	
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Unit test for the test functions
		
		Should probably figure out how to work with the unittest2 lib for Python...
		Until then, this works fine...
		"""
		print kwargs
		
		print "Testing calls from: %s" % __name__
		
		barcode = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", barcode
		
		if method == 'GET':
			got = self.getFunc(barcode)
		if method == 'POST':
			got = self.postFunc(barcode)
		if method == 'PUT':
			got = self.putFunc(barcode)
		if method == 'DELETE':
			got = self.deleteFunc(barcode)
			
		answer_json = json.loads(got)
		
		answer = answer_json['barcode']
		
		print "Got back: ", got
		
		try:
			if answer == barcode:
				print "%s: Passed" % str(method)
		except:
			print "%s: FAILED" % str(method)


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()