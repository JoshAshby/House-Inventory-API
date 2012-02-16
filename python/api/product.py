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
from productDocument import *
from ashpic import *
import productView
import baseObject

baseObject.urlReset()


@baseObject.route('/')
class total(baseObject.baseHTTPObject):
	'''
	Returns and manipulates the total product database.
	'''
	def get(self, *args, **kwargs):
		'''
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
		
		totals = {'data': name}
			
		view = productView.totalView(data=totals)
		
		return view.returnData()
		
	def post(self, *args, **kwargs):
		'''
		POST verb call
		
		Args:
		Returns:
			A JSON object like: {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53}
	
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode')
		
		if bar:
			tests = database.view("products/admin", key=bar).all()
			if tests:
				inform = json.dumps({'copy': bar})
				return inform
			
			product = productDoc(barcode=bar)
			
			name = self.hasMember('name', True)
			if name: product.name = name
			
			description = self.hasMember('description', True)
			
			quantity = self.hasMember('quantity', True)
			if quantity: product.quantity = int(quantity)
			
			cat = self.hasMember('cat', True)
			if cat: product.category = cat
			
			tags = self.hasMember('tags', True)
			if tags: product.tags = tags
			
			picTrue = self.hasMember('picTrue', True)
			if picTrue: pictureTrue = int(picTrue)
			else: pictureTrue = None
			pic = self.hasMember('picture', True)
			
			if pictureTrue is not None:
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
				product.picture = frodo
			
			if description:
				desc = description
				p = re.compile('\+')
				found = p.sub( ' ', desc)
				product.description = found
			
			product.barcode = bar
			product.save()

			name = database.view("products/all", key=bar).all()
			
			data = name[0]['value']
			view = productView.infoView(data=data)
		
			return view.returnData()
			
		else:
			view = productView.errorView({'error': 'Not enough data', 'missing': 'barcode'})
			
			return view.returnData()


@baseObject.route("/(.*)/")
class info(baseObject.baseHTTPObject):
	'''
	Product manipulation class. Functions to return the info, update and delete products are contained below, including a testing function for unittests.
	'''
	def get(self, *args, **kwargs):
		'''
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"product": {"category": "Notebook", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "tags": ["paper", "notebook", "graph", "graph paper"], "barcode": "718103025027", "quantity": 1, "name": "Green Graph Composition"}}
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode', None)
		
		name =  database.view("products/all", key=bar).first()
		
		name = dict(name)
		
		view = productView.infoView(data=name)
		
		return view.returnData()
	
	def put(self, *args, **kwargs):
		'''
		PUT verb call
		
		Args:
		Returns:
			A JSON object like: {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53}
	
		Where:
			oldbarcode = the previous barcode incase the barcode was changed.
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode', None)
		
		if bar:
			tests = database.view("products/admin", key=bar).all()
			if tests:
				inform = json.dumps({'copy': bar})
				return inform
			
			product = productDoc(barcode=bar)
			
			name = self.hasMember('name', True)
			if name: product.name = name
			
			description = self.hasMember('description', True)
			
			quantity = self.hasMember('quantity', True)
			if quantity: product.quantity = int(quantity)
			
			cat = self.hasMember('cat', True)
			if cat: product.category = cat
			
			tags = self.hasMember('tags', True)
			if tags: product.tags = tags
			
			picTrue = self.hasMember('picTrue', True)
			if picTrue: pictureTrue = int(picTrue)
			else: pictureTrue = None
			pic = self.hasMember('picture', True)
			
			if pictureTrue is not None:
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
				product.picture = frodo
			
			if description:
				desc = description
				p = re.compile('\+')
				found = p.sub( ' ', desc)
				product.description = found
			
			product.barcode = bar
			product.save()
			
			tryal = product.stock(quantity)
			
			name = database.view("products/all", key=bar).all()
			
			data = {'data': name[0]['value']}
			view = productView.infoView(data=data)
		
			return view.returnData()
			
		else:
			view = productView.errorView({'error': 'Not enough data', 'missing': 'barcode'})
			
			return view.returnData()
		
	def delete(self, *args, **kwargs):
		'''
		DELETE verb call
		
		Args:
		Returns
			A JSON object like: {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52, "thumb": "dog_thumb.png"}
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode', None)
		
		name = database.view("products/all", key=bar).first()['value']
		
		name['deleted'] = 'true'
		
		a = database.view("products/admin", key=bar).first()['value']['_id']
		
		database.delete_doc(a)
			
		view = productView.infoView(data=name)


app = web.application(baseObject.urls, globals())