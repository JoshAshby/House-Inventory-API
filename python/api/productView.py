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
from ashpic import *
from productDocument import *

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import datetime

from Cheetah.Template import Template

from reportlab.platypus import *

class infoView(object):
	def __init__(self, data):
		self.data = data
	
	def PDF(self):
		pass
		
	def HTML(self):
		page = Template(file="template/info.html", searchList=[self.data])
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({'product': self.data})
	
	def graph(self):
		buffer = StringIO()
		
		fig = plt.figure()
		ax = fig.add_subplot(111)

		product = productDoc.view("products/admin", key=self.data['barcode']).first()

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

		fig.savefig(buffer, format='png')

		graph = buffer.getvalue()
		buffer.close()
		
		return graph

class totalView(object):
	def __init__(self, data):
		self.data = data
	
	def PDF(self):
		pass
		
	def HTML(self):
		print self.data
		page = Template(file="template/total.html", searchList=[{"data": self.data, "title": "<b>Total Inventory</b>", 'type': 'Total Inventory'}])
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"total": self.data})