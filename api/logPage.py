#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Main admin functions

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import re
import time
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
	def get(self):	
		'''
		GET verb call
		
		Returns:
			A JSON object like: 
		'''
		bar = self.hasMember('barcode')
		
		log = productDoc.view("products/admin", key=bar).first()['log']
		
		web.header('Content-Type', 'application/json')
		
		return json.dumps({"log": log})
			

app = web.application(baseObject.urls, globals())
