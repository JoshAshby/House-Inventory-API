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
import re
import time
import datetime
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
from ashmath import *
from ashpic import *
import auth
import account
import stats

urls = (
	'', 'slash',
	'/', 'total',
	'/(.*)/', 'info'
)

class info:
	'''
	class documentation
	
	Product manipulation class. Functions to return the info, update and delete products are contained below, including a testing function for unittests.
	'''
	
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"product": {"category": "Notebook", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "tags": ["paper", "notebook", "graph", "graph paper"], "barcode": "718103025027", "quantity": 1, "name": "Green Graph Composition"}}
		'''
		try: 
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		name = database.view("products/all", key=bar).first()['value']
		inform = json.dumps({"product": name})
		
		if spam:
			web.header('Content-Type', 'application/json')
		return inform
	
	def postFunc(self, **kwargs):
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
			A JSON object like: {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53}
	
		Where:
			oldbarcode = the previous barcode incase the barcode was changed.
		'''
		try:
			bobbins= web.input(picture={})
		except:
			bobbins = kwargs
			if 'picture' in bobbins: pass
			else: bobbins['picture'] = {}
		
		if bobbins['barcode']:
			bar = bobbins['barcode']
			
			product = productDoc.view("products/admin", key=bar).first()
			#pro = database.view("products/all", key=bar).first()['value']
			
			if 'name' in bobbins: product.name = bobbins['name']
			
			if 'cat' in bobbins: product.category = bobbins['cat']
			
			if 'tags' in bobbins: product.tags = json.loads(bobbins['tags'])
			
			if 'picTrue' in bobbins: pictureTrue = int(bobbins['picTrue'])
			else: pictureTrue = 0
			pic = bobbins['picture']
			
			if pictureTrue == 1:
				catdog = re.search('(\..*)', pic.filename).group()
				
				frodo = bar + catdog
				
				f = open(abspath + '/pictures/' + frodo, "wb")

				while 1:
					chunk = pic.file.read(10000)
					if not chunk:
						break
					f.write( chunk )
				f.close()
				
				goop = freyaPics(frodo)
				goop.odinsThumb()
			else:
				try:
					frodo = product.picture
				except:
					frodo = "null"

			if 'description' in bobbins:
				desc = bobbins['description']
				p = re.compile('\+')
				found = p.sub( ' ', desc)
				product.description = found
			
			product.picture = frodo
			
			product.barcode = bar
			product.save()
			
			#incase the product is being restocked, run the machine learning stuff
			#if not then just change the value of the quantity 
			if int(bobbins['quantity']) > product.quantity:
				stats.restock(bar, int(bobbins['quantity']))
			else:
				product.quantity = int(bobbins['quantity'])
				product.log.append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": int(bobbins['quantity'])})
				product.save()

			name = database.view("products/all", key=bar).all()
			inform = json.dumps({"product": name[0]['value']})
			
			if spam:
				web.header('Content-Type', 'application/json')
			return inform
		else:
			return json.dumps({'error': 'Not enough data'})
		
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns
			A JSON object like: {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52, "thumb": "dog_thumb.png"}
		'''
		try: 
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		name = database.view("products/all", key=bar).first()['value']
		
		name['deleted'] = 'true'
		
		reply = {'product': name}
		
		inform = json.dumps(reply)
		
		a = database.view("products/admin", key=bar).first()['value']['_id']
		
		database.delete_doc(a)
		
		if spam:
			web.header('Content-Type', 'application/json')
		return inform
	
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
		
		
class total:
	'''
	class documentation
	
	Returns and manipulates the total product database.
	'''
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"total": [{"category": "Notebook", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "tags": ["paper", "notebook", "graph", "graph paper"], "barcode": "3037921120217", "quantity": 1, "name": "Orange Graph Composition"}, {"category": "Notebook", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "tags": ["paper", "notebook", "graph", "graph paper"], "barcode": "718103025027", "quantity": 1, "name": "Green Graph Composition"}, {"category": "Animal", "description": "A dog of god", "tags": ["Beagle", "dog", "pet"], "barcode": "dog987", "quantity": "2", "name": "Dog"}]}
		'''
		name = database.view("products/all").all()
		for i in range(len(name)):
			name[i] = name[i]['value']
		inform = json.dumps({'total': name})
		
		if spam:
			web.header('Content-Type', 'application/json')
		return inform
		
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
			A JSON object like: {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53}
	
		'''
		try:
			bobbins= web.input(picture={})
		except:
			bobbins = kwargs
			if 'picture' in bobbins: pass
			else: bobbins['picture'] = {}
		
		if bobbins['barcode']:
			bar = bobbins['barcode']
				
			tests = database.view("products/all", key=bar).all()
			if tests:
				inform = json.dumps({'copy': bar})
				if spam:
					web.header('Content-Type', 'application/json')
				return inform
			
			#product = productDoc.view("products/admin", key=bar).first()
			product = productDoc(barcode=bar)
			
			if 'name' in bobbins: product.name = bobbins['name']
			
			if 'description' in bobbins: product.description = bobbins['description']
			
			if 'quantity' in bobbins: product.quantity = bobbins['quantity']
			
			if 'cat' in bobbins: product.category = bobbins['cat']
			
			if 'tags' in bobbins: product.tags = json.loads(bobbins['tags'])
			
			if 'picTrue' in bobbins: pictureTrue = int(bobbins['picTrue'])
			else: pictureTrue = 0
			pic = bobbins['picture']
			
			if pictureTrue == 1:
				catdog = re.search('(\..*)', pic.filename).group()
				
				frodo = bar + catdog
				
				f = open(abspath + '/pictures/' + frodo, "wb")

				while 1:
					chunk = pic.file.read(10000)
					if not chunk:
						break
					f.write( chunk )
				f.close()
				
				goop = freyaPics(frodo)
				goop.odinsThumb()
			else:
				frodo = "null"
			
			if 'description' in bobbins:
				desc = bobbins['description']
				p = re.compile('\+')
				found = p.sub( ' ', desc)
				product.description = found
			
			product.picture = frodo
			
			product.barcode = bar
			product.save()

			name = database.view("products/all", key=bar).all()
			inform = json.dumps({"product": name[0]['value']})
			
			if spam:
				web.header('Content-Type', 'application/json')
			return inform
		else:
			return json.dumps({'error': 'Not enough data'})
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		pass
		
	def deleteFun(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		pass
	
	def GET(self):
		'''
		function documentation
		
		Returns the given products info in JSON format
		
		Returns:
		'''
		return self.getFunc()
	
	@auth.oauth_protect
	def POST(self):
		'''
		function documentation
		
		Adds a new product
		
		Returns: 
		'''
		return self.postFunc()
	
	@auth.oauth_protect
	def PUT(self):
		'''
		function documentation
		
		Updates the current product according to the included data.
		
		Returns:
		'''
		return self.putFunc()
	
	@auth.oauth_protect
	def DELETE(self):
		'''
		function documentation
		
		Deletes the current product, and moves its data into the restore database.
		
		Returns: None
		'''
		return self.deleteFunc()
		

app = web.application(urls, globals(), autoreload=False)
#application = app.wsgifunc()