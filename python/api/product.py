#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main public product calls
Does not involve anything with categories, all that is in cat.py

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

urls = (
	'', 'slash',
	'/(.*)/info/', 'info',
	'/', 'total',
	'/names/', 'names'
)

class slash:
	def GET(self): raise web.seeother("/")

class info:
	'''
	class documentation
	Info about the given product.
	
	Returns:
		A JSON object like: {"picture": "dog.png", "description": "a dog of god", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 10, "id": 52}
	'''
		
	def endFunc(self, barcode):
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
	
	def GET(self, barcode):
		return self.endFunc(barcode)
		
	def POST(self, barcode):
		return self.endFunc(barcode)
		
		
class total:
	'''
	class documentation
	Returns all the product info. Used for product info tables in the main client.
	
	Returns:
		A JSON object like: {"total" : [{"picture": "718103025027.png", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "barcode": "718103025027", "name": "Green Graph Composition", "flag": "M", "quantity": 1, "id": 3, "thumb": "718103025027_thumb.png"}, {"picture": "3037921120217.png", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "barcode": "3037921120217", "name": "Orange Graph Notebook", "flag": "L", "quantity": 1, "id": 4, "thumb": "3037921120217_thumb.png"}]}
	'''
	
	def endFunc(self):
		query = []
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"total": query})
		
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()
		

class names:
	'''
	class documentation
	Generates a list of names and barcodes for auto complete.
	
	Returns:
		A JSON object like: {"names" : [{"barcode": "718103025027", "name": "Green Graph Composition"}, {"barcode": "3037921120217", "name": "Orange Graph Notebook"}, {"barcode": "043396366268", "name": "the social network"}, {"barcode": "dog987", "name": "Beagle"}]}
	'''
		
	def endFunc(self):
		query = []
		names = db.query('SELECT `name`, `barcode` FROM `products`')
		for i in range(len(names)):
			query.append(names[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"names": query})
	
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()
		

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()