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
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
#import adminTag

urls = (
	'', 'slash',
	'/', 'tags_total',
	'/(.*)/', 'tags_info'
	#'/(.*)/stats/', adminTag.app
)

class slash:
	def GET(self): raise web.seeother("/")

class tags_info:
	'''
	class documentation
	Returns all the products in a tag
	
	Returns:
		A JSON object like: {"products" : [{"barcode": "dog987", "name": "A dog", "picture": "dog.png"}]}
	'''
	
	def endFunc(self, tags):
		query = []
		name = db.query('SELECT `barcode`, `name`, `picture` FROM `products` WHERE `tags` LIKE "%'+ tags +'%"')
		
		for i in range(len(name)):
			query.append(name[i])
		
		print query
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'products': query})
		
	def GET(self, cat):
		return self.endFunc(cat)
		
	def POST(self, cat):
		return self.endFunc(cat)


class tags_total:
	'''
	class documentation
	Returns all the tags.
	
	Returns:
		A JSON object like: {"tags" : ["abc", "def"]}
	'''
		
	def endFunc(self):
		query = []
		dog = []
		woof = []
		name = db.query('SELECT `tags` FROM `products`')
		for i in range(len(name)):
			query.append(json.loads(name[i]['tags']))
		
		for x in range(len(query)):
			for z in range(len(query[x])):
				dog.append(query[x][z])
		
		queryFix = list(set(dog))
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'tags': queryFix})
	
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()

		
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()