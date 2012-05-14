#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
productDoc database document class

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import couchdbkit
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