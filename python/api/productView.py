#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Product information views

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

from pdfView import *
from htmlView import *

class infoView(object):
	def __init__(self, data):
		self.data = data
		self.data['type'] = "productInfo"
	
	def PDF(self):
		preReport = pdfView(self.data)
		
		report = preReport.build()
		
		web.header('Content-Type', 'application/pdf')
		return report
		
	def HTML(self):
		prePage = htmlView(self.data)
		
		page = prePage.build()
		
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({'product': self.data})

class totalView(object):
	def __init__(self, data):
		self.data = data
		self.data['type'] = "productTotal"
	
	def PDF(self):
		preReport = pdfView(self.data)
		
		report = preReport.build()
		
		web.header('Content-Type', 'application/pdf')
		return report
		
	def HTML(self):
		prePage = htmlView(self.data)
		
		page = prePage.build()
		
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"total": self.data['data']})