#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
A test sub app for messing around with new things and what not before I decide to use them or not.

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import math
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
import baseObject

baseObject.urlReset()


@baseObject.route('/(.*)/')
class test(baseObject.baseHTTPObject):
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
		'''
		self.members(*args, **kwargs)
		bar = self.hasMember('barcode')
		
		pass


app = web.application(baseObject.urls, globals())
