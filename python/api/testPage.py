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
import auth

urls = (
	"", "slash",
	"/(.*)/", "test"
)

class test:
	'''
	class documentation
	
	Testing page object. Functions include full REST with OAuth protection on the POST PUT DELETE calls.
	Testing frameowrk for unittests included.
	'''
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		try:
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		query=[]
		
		name = db.select('stats', where='barcode=$barcode', vars={'barcode': bar}, _test=False)
	
		for i in range(len(name)):
			query.append(name[i])
		
		all = json.loads(query[0]['all'])
		last_5 = json.loads(query[0]['last_5'])
		set_all = list(set(all))
		leng = len(set_all)
		
		added = 0
		for q in range(leng):
			added += set_all[q]
			
		avg = added/(leng)
		
		prestd = 0
		for s in range(leng):
			setr = math.pow((set_all[s] - avg), 2)
			prestd += setr
		
		stddv = math.sqrt(prestd/leng)
		
		reply = {
			"barcode": bar,
			'last_5': last_5,
			#'all': all,
			'balanced': set_all,
			'avg': avg,
			'stddv': stddv
		}
		
		answer = json.dumps(reply)
		
		return answer
	
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(barcode=kwargs['barcode'])
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(barcode=kwargs['barcode'])
	
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Returns:
			whatever I tell it to since it's a testing page...
		'''
		return self.getFunc(barcode=kwargs['barcode'])
	
	def GET(self, bar):
		return self.getFunc(barcode=bar)
	
	@auth.oauth_protect
	def POST(self):
		return self.postFunc()
	
	@auth.oauth_protect
	def PUT(self):
		return self.putFunc()
	
	@auth.oauth_protect
	def DELETE(self):
		return self.deleteFunc()


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()