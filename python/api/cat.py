#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Category sub-app for handeling all category API calls...

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import couchdbkit
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
	'/', 'catTotal',
	'/(.*)/tag/(.*)/', 'catTag',
	'/(.*)/', 'catInfo'
)

class catInfo:
	'''
	class documentation
	
	Category maniplulation object'''
	
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			cat - the cateogry
		Returns:
		'''
		try:
			wi = web.input()
			cat = wi['category']
		except:
			cat = kwargs['category']
			
		query = []
		name = db.query('SELECT `barcode`, `name`, `picture`, `tags` FROM `products` WHERE `cat` = $cat', vars = {'cat': cat})
		for i in range(len(name)):
			query.append(name[i])
		
		for s in range(len(query)):
			query[s]['tags'] = json.loads(query[s]['tags'])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'products': query})
		
	def postFunc(self, **kargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		pass
		
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		pass
		
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		pass
		
	def GET(self, cat):
		return self.getFunc(category=cat)
	
	@auth.oauth_protect
	def POST(self, cat):
		return self.postFunc(category=cat)
	
	@auth.oauth_protect
	def PUT(self, cat):
		return self.putFunc(category=cat)
	
	@auth.oauth_protect
	def DELETE(self, cat):
		return self.deleteFunc(category=cat)
		
		
class catTotal:
	'''
	class documentation
	
	Category maniplulation object
	'''
	
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Args:
		Returns:
		'''
		query = []
		name = database.view("products/admin").all()
		
		for i in range(len(name)):
			query.append(name[i]['value']['category'])
			
		queryFix = list(set(query))
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'categories': queryFix})
	
	def postFunc(self, **kargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		pass
		
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		pass
		
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		pass
		
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
		

class catTag:
	'''
	class documentation
	
	Category maniplulation object
	'''
	
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Args:
		Returns:
		'''
		try:
			wi = web.input()
			cat = wi['category']
			tag = wi['tag']
		except:
			cat = kwargs['category']
			tag = kwargs['tag']
			
		query = []
		dog = []
		#name = db.query('SELECT `tags`, `barcode`, `name`, `picture` FROM `products` WHERE `cat` = $cat', vars = {'cat': cat})
		name = db.select('products', where='cat=$cat', what='tags, barcode, name, picture', vars={'cat':cat}, _test=False)
		
		for i in range(len(name)):
			query.append(name[i])
		
		for x in range(len(query)):
			e = json.loads(query[x]['tags'])
			for z in range(len(e)):
				if e[z] == tag:
					dog.append(query[x])
				else: pass
		
		for f in range(len(dog)):
			dog[f]['tags'] = json.loads(dog[f]['tags'])
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'products': dog})
	
	def postFunc(self, **kargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		pass
		
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		pass
		
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		pass
		
	def GET(self, cat, tags):
		return self.getFunc(category=cat, tag=tags)
	
	@auth.oauth_protect
	def POST(self, cat, tags):
		return self.postFunc(category=cat, tag=tags)
	
	@auth.oauth_protect
	def PUT(self, cat, tags):
		return self.putFunc(category=cat, tag=tags)
	
	@auth.oauth_protect
	def DELETE(self, cat, tags):
		return self.deleteFunc(category=cat, tag=tags)
		
		
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()