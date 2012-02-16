#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main admin functions

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
import baseObject

baseObject.urlReset()

@baseObject.route('/(.*)/')
class log(baseObject.baseHTTPObject):
	'''
	Generates the use log about the given product.
	'''		
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			A JSON object like: 
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode')
		
		log = productDoc.view("products/admin", key=bar).first()['log']
		
		if spam:
			web.header('Content-Type', 'application/json')
		
		return json.dumps({"log": log})
			

app = web.application(baseObject.urls, globals())
