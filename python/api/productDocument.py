#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
productDoc database document class

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import json
import re
import time
import math
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
from dateutil.relativedelta import relativedelta

class productDoc(couchdbkit.Document):
	barcode = couchdbkit.StringProperty()
	picture = couchdbkit.StringProperty()
	name = couchdbkit.StringProperty()
	doc_type = couchdbkit.StringProperty()
	category = couchdbkit.StringProperty()
	description = couchdbkit.StringProperty()
	flag = couchdbkit.StringProperty()
	
	doc_type = "productDoc"
	
	quantity = couchdbkit.IntegerProperty()
	rank = couchdbkit.IntegerProperty
	
	tags = couchdbkit.ListProperty()
	log = couchdbkit.ListProperty()
	
	restock = couchdbkit.DictProperty()
	prediction = couchdbkit.DictProperty()
	
	def stock(self, restockQuantity):
		'''
		First we need to go through and make a new prediction using the deltas and the normalized quantitys
		This is then used to make a prediction about when the product is going to run out, based off of the newly
		added stock.
		Then we have to go through and add the entry to the log, reset the quantity, and change the restock date
		and quantity to the new set.
		After all of this is done, the prediction is returned, so that the call can throw it in with the rest of the returned
		JSON data.
		
		We also have to make sure we are pulling the normalized quantity and are storing it too. This is done by taking
		the new quantity and dividing it by the restock quantity to get a number between 0 and 1. This is done to make
		sure that descrepancies with the quantitys are all the same, for example, if you had a set of 10 units and then
		restocked with 60, the algorithm would think that the prediction should be lower just because of the fact that
		the 10 units probably took less time to be used than will/did the 60 units. (if this all makes sense).
		'''
		a = self.log
		
		query = sorted(a, key=lambda a: a['delta'], reverse=True)

		delta = []
		quantity = []
		norm = []

		for key in range(len(query)):
			delta.append(query[key]['delta'])
			quantity.append(query[key]['quantity'])
			norm.append(query[key]['norm'])
		
		# Start of the linear regression algorithm to predict the DoZ
		
		x = []
		y = []
		
		length = len(delta)
		
		xBar = 0.00
		yBar = 0.00
		xyBar = 0.00
		x2Bar = 0.00
		xBar2 = 0.00
		
		for q in range(length):
			xBar += delta[q]
			yBar += norm[q]
			xyBar += delta[q] * norm[q]
			x2Bar += math.pow(delta[q], 2)
		
		xBar = xBar / length
		yBar = yBar / length
		xyBar = xyBar / length
		x2Bar = x2Bar / length
		xBar2 = math.pow(xBar, 2)
		
		m = (xBar * yBar - xyBar) / ( xBar2 - x2Bar)
		b = yBar - m * xBar
		
		predicted = (-b/m)
		
		'''
		This is here for when I'm ready to start storing previous prediction lines,
		for z in range(int(predicted + 0.5) + 2):
			x.append(z)
			y.append(m * z + b)
		'''
		# End algorithm
		
		self.prediction['m'] = m
		self.prediction['b'] = b
		
		additionalData = {"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": self.quantity + restockQuantity, "delta": 0, "norm": 1}
		self.log.append(additionalData)
		
		self.restock['date'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
		self.restock['quantity'] =  self.quantity + restockQuantity
		
		self.quantity = self.quantity + restockQuantity
		
		m = m * max(quantity)
		#b = b * max(quantity)
		b = restockQuantity * 0.90
		
		predicted = (-b/m)
		
		self.prediction['predicted'] = predicted
		
		self.save()
		
		return predicted
		
		
	def order(self, quantity):
		self.quantity = self.quantity - restockQuantity
		additionalData = {"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": self.quantity, "delta": (datetime.datetime.now() - datetime.datetime.strptime(self.restock['date'], "%Y-%m-%d %H:%M:%S")).days(), "norm": (self.quantity / self.restock['quantity'])}
		self.log.append(additionalData)
		self.save()


productDoc.set_db(database)