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

'''
From: http://webpy.org/install and http://code.google.com/p/modwsgi/wiki/ApplicationIssues
This must be done to avoid the import errors which come up with having linear.py and config.py
'''
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
#import adminCat

urls = (
	'', 'slash',
	'/', 'cat_total',
	'/(.*)/info/', 'cat_info',
	'/(.*)/tag/', 'catTags',
	'/(.*)/tag/(.*)/', 'catTagsInfo'
	#'/(.*)/stats/', adminCat.app
)

class slash:
	def GET(self): raise web.seeother("/")

class cat_info:
	'''
	class documentation
	Returns all the products in a category.
	
	Returns:
		A JSON object like: {"products" : [{"barcode": "dog987", "name": "A dog", "picture": "dog.png"}]}
	'''
	
	def endFunc(self, cat):
		query = []
		name = db.query('SELECT `barcode`, `name`, `picture`, `tags` FROM `products` WHERE `cat` = $cat', vars = {'cat': cat})
		for i in range(len(name)):
			query.append(name[i])
		
		for s in range(len(query)):
			query[s]['tags'] = json.loads(query[s]['tags'])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'products': query})
		
	def GET(self, cat):
		return self.endFunc(cat)
		
	def POST(self, cat):
		return self.endFunc(cat)


class cat_total:
	'''
	class documentation
	Returns all the categories.
	
	Returns:
		A JSON object like: {"categories" : ["abc", "def"]}
	'''
		
	def endFunc(self):
		query = []
		name = db.query('SELECT `cat` FROM `products`')
		for i in range(len(name)):
			query.append(name[i]['cat'])
		queryFix = list(set(query))
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'categories': queryFix})
	
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()


class catTags:
	'''
	class documentation
	Returns all the tags in a category.
	
	Returns:
		A JSON object like: {"tags" : ["abc", "def"]}
	'''
		
	def endFunc(self, cat):
		query = []
		dog = []
		name = db.query('SELECT `tags` FROM `products` WHERE `cat` = $cat', vars = {'cat': cat})
		
		for i in range(len(name)):
			query.append(json.loads(name[i]['tags']))
		
		for x in range(len(query)):
			for z in range(len(query[x])):
				dog.append(query[x][z])
		
		queryFix = list(set(dog))
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({'tags': queryFix})
	
	def GET(self, cat):
		return self.endFunc(cat)
		
	def POST(self, cat):
		return self.endFunc(cat)


class catTagsInfo:
	'''
	class documentation
	Returns all the tags in a category.
	
	Returns:
		A JSON object like: {"tags" : ["abc", "def"]}
	'''
		
	def endFunc(self, cat, tag):
		query = []
		dog = []
		name = db.query('SELECT `tags`, `barcode`, `name`, `picture` FROM `products` WHERE `cat` = $cat', vars = {'cat': cat})
		
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
	
	def GET(self, cat, tag):
		return self.endFunc(cat, tag)
		
	def POST(self, cat, tag):
		return self.endFunc(cat, tag)
		
		
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()