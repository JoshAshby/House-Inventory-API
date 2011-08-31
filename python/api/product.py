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
try:
	from configSub import *
except:
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
from configSub import *

urls = (
	'', 'slash',
	'/(.*)/', 'info',
	'/', 'total',
	'/names/', 'names'
)

class slash:
	def GET(self): raise web.seeother("/")

class info:
	'''
	class documentation
	
	Product manipulation class. Functions to return the info, update and delete products are contained below, including a testing function for unittests.
	'''
	
	def getFunc(self, *args):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"picture": "dog.png", "description": "a dog of god", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 10, "id": 52}
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		if debug: barcode = args[0]
		else:
			try:
				wi = web.input()
				barcode = wi['barcode']
			except:
				barcode = args[0]
		
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
	
	def postFunc(self, *args):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		return self.getFunc(args)
	
	def putFunc(self, *args):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		return self.getFunc(args)
		
	def deleteFun(self, *args):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		return self.getFun(args)
	
	def GET(self, barcode):
		'''
		function documentation
		
		Returns the given products info in JSON format
		
		Returns:
		'''
		return self.getFunc(barcode)
	
	@auth.oauth_protect
	def POST(self, barcode):
		'''
		function documentation
		
		Currently does nothing
		
		Returns: None
		'''
		pass
		#return self.postFunc(barcode)
	
	@auth.oauth_protect
	def PUT(self, barcode):
		'''
		function documentation
		
		Updates the current product according to the included data.
		
		Returns:
		'''
		return self.putFunc(barcode)
	
	@auth.oauth_protect
	def DELETE(self, barcode):
		'''
		function documentation
		
		Deletes the current product, and moves its data into the restore database.
		
		Returns:
		'''
		return self.deleteFunc(barcode
	
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print kwargs
		
		print "Testing calls from: %s" % __name__
		
		barcode = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", barcode
		
		if method == 'GET':
			#We just need the barcode since we're getting info about the product.
			got = self.getFunc(barcode)
		if method == 'POST':
			#Doesn't do anything right now...
			got = self.postFunc(barcode)
		if method == 'PUT':
			#We have to get all the update info so make sure it's all passed...
			got = self.putFunc(barcode)
		if method == 'DELETE':
			#We just need the barcode for this one since it's just to delete the product...
			got = self.deleteFunc(barcode)
			
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['barcode']
		
		print "Got back: ", got
		
		try:
			if answer == barcode:
				print "%s: Passed" % str(method)
		except:
			print "%s: FAILED" % str(method)
		
		
class total:
	'''
	class documentation
	
	Returns and manipulates the total product database.
	'''
	def getFunc(self, *args):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"total" : [{"picture": "718103025027.png", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "barcode": "718103025027", "name": "Green Graph Composition", "flag": "M", "quantity": 1, "id": 3, "thumb": "718103025027_thumb.png"}, {"picture": "3037921120217.png", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "barcode": "3037921120217", "name": "Orange Graph Notebook", "flag": "L", "quantity": 1, "id": 4, "thumb": "3037921120217_thumb.png"}]}
		'''
		query = []
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"total": query})
		
	def postFunc(self, *args):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		return self.getFunc(args)
	
	def putFunc(self, *args):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		return self.getFunc(args)
		
	def deleteFun(self, *args):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		return self.getFun(args)
	
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
		#return self.postFunc()
	
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
		pass
		#return self.deleteFunc()
	
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print kwargs
		
		print "Testing calls from: %s" % __name__
		
		barcode = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", barcode
		
		if method == 'GET':
			#We just need the barcode since we're getting info about the product.
			got = self.getFunc(barcode)
		if method == 'POST':
			#Doesn't do anything right now...
			got = self.postFunc(barcode)
		if method == 'PUT':
			#We have to get all the update info so make sure it's all passed...
			got = self.putFunc(barcode)
		if method == 'DELETE':
			#We just need the barcode for this one since it's just to delete the product...
			got = self.deleteFunc(barcode)
			
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['barcode']
		
		print "Got back: ", got
		
		try:
			if answer == barcode:
				print "%s: Passed" % str(method)
		except:
			print "%s: FAILED" % str(method)
		

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()