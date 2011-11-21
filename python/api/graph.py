#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
A graphing sub app to return various graphs in png format from the product data.
This may later on also do PDF reports for the whole inventory or a product

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
import auth

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import datetime

urls = (
	"", "slash",
	"/(.*)/", "graph"
)

class graph:
	'''
	class documentation
	
	Current'y generates graphs for the product log
	'''
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
			A png formated graph of the product log 
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		try:
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		buffer = StringIO()
		
		fig = plt.figure()
		ax = fig.add_subplot(111)

		product = productDoc.view("products/admin", key=bar).first()

		a = product.log

		query = sorted(a, key=lambda a: a['date'], reverse=True)

		date = []
		quantity = []

		for key in range(len(query)):
			date.append(datetime.datetime.strptime(query[key]['date'], '%Y-%m-%d %H:%M:%S'))
			quantity.append(query[key]['quantity'])

		ax.plot(date, quantity)

		ax.xaxis.set_major_locator( MonthLocator() )
		ax.xaxis.set_major_formatter( DateFormatter('%m-%Y') )

		ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
		fig.autofmt_xdate()

		fig.savefig(buffer)

		graph = buffer.getvalue()
		buffer.close()
		
		web.header('Content-Type', "image/png")
		
		return graph
	
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Returns:
			Nothing
		'''
		pass
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Returns:
			Nothing
		'''
		pass
	
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Returns:
			Nothing
		'''
		pass
	
	def GET(self, bar):
		return self.getFunc(barcode=bar)
	
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
