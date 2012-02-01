#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Tags sub-app for handeling all tag API calls...

Neat thing about tags is multiple tags can apply to a product, and it helps you narrow down with categories.
Even though tags act a lot like categories at first, the fact that you can look at a category, then find only a certian tag with in that category is really
powerful.

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

from productDocument import *

import tagView

urls = (
	'', 'slash',
	'/', 'tagsTotal',
	'/(.*)/', 'tagsInfo'
)

class tagsInfo:
	'''
	class documentation
	
	Returns all the products in a tag
	'''
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		wi = web.input()
		try:
			tag = wi['tag']
		except:
			tag = kwargs['tag']
		
		query = database.view("cattag/tags", key=tag).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
			
		query = {'data': query}
		
		view = tagView.infoView(query, wi)
		
		return view.returnData()
	
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
	
	def GET(self, ta):
		return self.getFunc(tag=ta)
	
	def POST(self, ta):
		return self.postFunc(tag=ta)
	
	def PUT(self, ta):
		return self.putFunc(tag=ta)
	
	def DELETE(self, ta):
		return self.deleteFunc(tag=ta)


class tagsTotal:
	'''
	class documentation
	
	Returns all the tags.
	'''
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
			A JSON object like: {"tags" : ["abc", "def"]}
		'''
		wi = web.input()
		dog = []
		query = database.view("products/admin").all()
		
		for x in range(len(query)):
			for z in range(len(query[x]['value']['tags'])):
				dog.append(query[x]['value']['tags'][z])
		
		queryFix = list(set(dog))
		
		queryFinal = {'data': queryFix}
		
		view = tagView.totalView(queryFinal, wi)
		
		return view.returnData()
	
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
	
	def GET(self):
		return self.getFunc()
	
	def POST(self):
		return self.postFunc()
	
	def PUT(self):
		return self.putFunc()
	
	def DELETE(self):
		return self.deleteFunc()

		
app = web.application(urls, globals(), autoreload=False)
#application = app.wsgifunc()
