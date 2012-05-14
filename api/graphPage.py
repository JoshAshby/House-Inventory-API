#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
A graphing sub app to return various graphs in png format from the product data.
This may later on also do PDF reports for the whole inventory or a product

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
from productDocument import *
import math
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import datetime
import baseObject

baseObject.urlReset()


@baseObject.route("/timeline/(.*)/")
class timelineGraph(baseObject.baseHTTPObject):
	'''
	Currently generates graphs for the product log
	'''
	def get(self, *args, **kwargs):	
		'''
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
		
		plt.xlabel('Date (Month-Year)')
		plt.ylabel('Quantity (Units)')
		
		plt.title('Quantity Change In Months (%s)' % bar)
		
		plt.grid(which='major', axis='both')
		
		fig.savefig(buffer)

		graph = buffer.getvalue()
		buffer.close()
		
		web.header('Content-Type', "image/png")
		
		return graph


@baseObject.route("/scatter/(.*)/")
class scatterGraph(baseObject.baseHTTPObject):
	'''
	
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			
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

		query = sorted(a, key=lambda a: a['delta'], reverse=True)

		delta = []
		quantity = []

		for key in range(len(query)):
			delta.append(query[key]['delta'])
			quantity.append(query[key]['norm'])
		
		# Start of the linear regression algorithm
		
		x = []
		y = []
		
		current = product.quantity
		length = len(delta)
		
		xBar = 0.00
		yBar = 0.00
		xyBar = 0.00
		x2Bar = 0.00
		xBar2 = 0.00
		
		for q in range(length):
			xBar += delta[q]
			yBar += quantity[q]
			xyBar += delta[q] * quantity[q]
			x2Bar += math.pow(delta[q], 2)
		
		xBar = xBar / length
		yBar = yBar / length
		xyBar = xyBar / length
		x2Bar = x2Bar / length
		xBar2 = math.pow(xBar, 2)
		
		m = (xBar * yBar - xyBar) / ( xBar2 - x2Bar)
		b = yBar - m * xBar
		
		predicted = (-b/m)
		
		for z in range(int(predicted + 0.5) + 2):
			x.append(z)
			y.append(m * z + b)
		
		# End algorithm
		
		ax.scatter(delta, quantity)
		ax.plot(x, y, 'm--')
		
		plt.xlim([-0.05, (predicted + 5)])
		plt.ylim([-0.05, 1.05])
		
		plt.xlabel('Delta (Days)')
		plt.ylabel('Normalized Quantity (0-1)')
		
		plt.title('Quantity Norm During Delta Days (%s)' % bar)
		
		plt.grid(which='major', axis='both')
		
		ax.annotate(('DoZ (~%f)' % predicted), xy=(predicted, 0), xycoords='data', xytext=(predicted - 4, 0.50), textcoords='data', arrowprops={'facecolor': 'black', 'shrink': 0.10})

		fig.savefig(buffer)

		graph = buffer.getvalue()
		buffer.close()
		
		web.header('Content-Type', "image/png")
		
		return graph


@baseObject.route("/cluster/quantity/")
class quantityClusterGraph(baseObject.baseHTTPObject):
	'''
	
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			
		'''
		buffer = StringIO()
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		
		date = []
		quantity = []
		
		names = database.view("products/admin").all()
		
		for i in range(len(names)):
			date.append(datetime.datetime.strptime(names[i]['value']['restock']['date'], '%Y-%m-%d %H:%M:%S').month)
			quantity.append(names[i]['value']['restock']['quantity'])
		
		ax.scatter(date, quantity)

		plt.xlabel('Month')
		plt.ylabel('Quantity')
		
		plt.title('General Restock During Time of Year')
		
		plt.grid(which='both', axis='both')
		
		ax.xaxis.set_minor_locator( MonthLocator(interval=1) )
		ax.xaxis.set_minor_formatter( DateFormatter('%m') )

		ax.fmt_xdata = DateFormatter('%m')
		fig.autofmt_xdate()
		
		plt.xlabel('Month')
		plt.ylabel('Quantity (Units)')
		
		plt.xlim([-0.50, 12.50])
		plt.ylim([0, (max(quantity) + 5)])
		
		fig.savefig(buffer)

		graph = buffer.getvalue()
		buffer.close()
		
		web.header('Content-Type', "image/png")
		
		return graph


@baseObject.route("/cluster/quantity/(.*)/")
class singleQuantityClusterGraph(baseObject.baseHTTPObject):
	'''
	
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			
		'''
		buffer = StringIO()
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		
		date = []
		quantity = []
		
		names = database.view("products/admin").all()
		
		for i in range(len(names)):
			date.append(datetime.datetime.strptime(names[i]['value']['restock']['date'], '%Y-%m-%d %H:%M:%S').month)
			quantity.append(names[i]['value']['restock']['quantity'])
		
		ax.scatter(date, quantity)

		plt.xlabel('Month')
		plt.ylabel('Quantity')
		
		plt.title('General Restock During Time of Year')
		
		plt.grid(which='both', axis='both')
		
		ax.xaxis.set_minor_locator( MonthLocator(interval=1) )
		ax.xaxis.set_minor_formatter( DateFormatter('%m') )

		ax.fmt_xdata = DateFormatter('%m')
		fig.autofmt_xdate()
		
		plt.xlabel('Month')
		plt.ylabel('Quantity (Units)')
		
		plt.xlim([-0.50, 12.50])
		plt.ylim([0, (max(quantity) + 5)])
		
		fig.savefig(buffer)

		graph = buffer.getvalue()
		buffer.close()
		
		web.header('Content-Type', "image/png")
		
		return graph
		

app = web.application(baseObject.urls, globals())
