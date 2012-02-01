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

from productDocument import *

import catView

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
		wi = web.input()
		try:
			cat = wi['category']
		except:
			cat = kwargs['category']
			
		query = database.view("cattag/categorys", key=cat).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
		
		totals = {'data': query}
		
		view = catView.infoView(totals, wi)
		
		return view.returnData()
		
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
	
	def POST(self, cat):
		return self.postFunc(category=cat)
	
	def PUT(self, cat):
		return self.putFunc(category=cat)
	
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
		wi = web.input()
		query = []
		name = database.view("products/admin").all()
		
		for i in range(len(name)):
			query.append(name[i]['value']['category'])
		
		
		queryFix = list(set(query))
		
		names = {'data': queryFix}
		
		view = catView.totalView(names, wi)
		
		return view.returnData()
	
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
	
	def POST(self):
		return self.postFunc()
	
	def PUT(self):
		return self.putFunc()
	
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
		wi = web.input()
		try:
			cat = wi['category']
			tag = wi['tag']
		except:
			cat = kwargs['category']
			tag = kwargs['tag']
			
		query = []
		dog = []
		
		query = database.view("cattag/categorys", key=cat).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
		
		for x in range(len(query)):
			e = query[x]['tags']
			for z in range(len(e)):
				if e[z] == tag:
					dog.append(query[x])
				else: pass
		
		dog = {'data': dog}
		
		view = catView.tagView(dog, wi)
		
		return view.returnData()
	
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
	
	def POST(self, cat, tags):
		return self.postFunc(category=cat, tag=tags)
	
	def PUT(self, cat, tags):
		return self.putFunc(category=cat, tag=tags)
	
	def DELETE(self, cat, tags):
		return self.deleteFunc(category=cat, tag=tags)
		
		
app = web.application(urls, globals(), autoreload=False)
#application = app.wsgifunc()
