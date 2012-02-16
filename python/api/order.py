#!/usr/bin/env python2
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
import datetime
import orderView
import baseObject

baseObject.urlReset()


@baseObject.route('/')
class placeOrder(baseObject.baseHTTPObject):
	'''
	'''
	def get(self, *args, **kwargs):
		'''
		GET verb call
		
		Returns:
			
		'''
		self.members(*args, **kwargs)
		user = self.hasMember('user')
		user = json.loads(self.hasMember('order'))
			
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
		
		view = orderView.orderView(data=ordered)
		
		return view.returnData()


@baseObject.route('/(.*)/')
class viewOrder(baseObject.baseHTTPObject):
	'''
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			A PDF HTML or JSON formated response accoriding to the attached type tag.
		'''
		self.members(*args, **kwargs)
		orderId = self.hasMember('id')
		
		order_doc = database.view("order/all", key=orderId).first()['value']
		
		view = orderView.infoView(data=order_doc)
		
		return view.returnData()
		

app = web.application(baseObject.urls, globals())
