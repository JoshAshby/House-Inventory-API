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
from productDocument import *
from orderDocument import *
import auth

import datetime

import orderView

urls = (
	"", "slash",
	"/", "placeOrder",
	"/(.*)/", "viewOrder"
)

class placeOrder:
	'''
	class documentation
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
			user = wi['user']
			orderWi = str(wi['order'])
			order = json.loads(orderWi)
			
		except:
			user = kwargs['user']
			order = json.loads(kwargs['order'])
			
		#go through and check things
		for bar in order:
			product = productDoc.view("products/admin", key=bar).first()
			
			if product.quantity > order[bar]:
				pass
			else:
				return json.dumps({"error": "Product quantity too low", "barcode": bar})
		
		order_doc = orderDoc()
		
		for bar in order:
			product = productDoc.view("products/admin", key=bar).first()
			
			product.order(order[bar])
		
		order_id = order_doc.genOrder(user, order)
		
		ordered = {"user": user, "order": order, "id": order_id}
		
		view = orderView.orderView(ordered)
		
		if 't' in wi: t = wi['t']
		elif 't' in kwargs: t = kwargs['t']
		else: t = 'json'
		
		if t == 'html':
			inform = view.HTML()
		elif t == 'json':
			inform = view.JSON()
		elif t == 'pdf':
			inform = view.PDF()
		return inform
	
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


class viewOrder:
	'''
	class documentation
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
			orderId = wi['id']
			
		except:
			orderId = kwargs['id']
		
		order_doc = database.view("order/all", key=orderId).first()['value']
		
		view = orderView.infoView(order_doc)
		
		if 't' in wi: t = wi['t']
		elif 't' in kwargs: t = kwargs['t']
		else: t = 'json'
		
		if t == 'html':
			inform = view.HTML()
		elif t == 'json':
			inform = view.JSON()
		elif t == 'pdf':
			inform = view.PDF()
		return inform
	
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
	
	def GET(self, orderId):
		return self.getFunc(id=orderId)
	
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
#application = app.wsgifunc()
