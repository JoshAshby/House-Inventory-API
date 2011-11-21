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
import couchdbkit

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
import os
from configSub import *

class orderDoc(couchdbkit.Document):
	id = couchdbkit.StringProperty()
	user = couchdbkit.StringProperty()
	doc_type = couchdbkit.StringProperty()
	
	doc_type = "orderDoc"
	
	order = couchdbkit.DictProperty()
	
	def genOrder(self, user, order):
		tempid = ''.join(map(lambda x:'0123456789'[ord(x)%10], os.urandom(10)))
		temp = orderDoc.view("order/admin", key=tempid).first()
		while temp:
			tempid = ''.join(map(lambda x:'0123456789'[ord(x)%10], os.urandom(10)))
			temp = orderDoc.view("order/admin", key=tempid).first()
		
		self.id = tempid
		self.user = user
		self.order = order
		
		self.save()
		
		return self.id

orderDoc.set_db(database)
