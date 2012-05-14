#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
PDF design view object

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
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

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import datetime

from productDocument import *

margin = .75*inch
indent = .25*inch
pageType = letter

class pdfView(object):
	def __init__(self, data):
		self.data = data
		self.styles=getSampleStyleSheet()
		self.styles.add(ParagraphStyle(name='Blue', textColor="#0067A5", leftIndent=indent))
		self.styles.add(ParagraphStyle(name='RedIndent', textColor="#B22222", leftIndent=(indent*2)))
		self.styles.add(ParagraphStyle(name='leftIndented', leftIndent=indent))
		self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
		
	def build(self):
		self.buffer = StringIO()
		
		self.doc = SimpleDocTemplate(self.buffer, pagesize=pageType,
					rightMargin=margin,leftMargin=margin,
					topMargin=margin,bottomMargin=margin)
		self.Story=[]
		logo = "template/css/images/ring.png"
		formatted_time = time.ctime()
		
		ptext = "<img src='template/css/images/ring.png' width='50' height='50' /><font size=6>Report generated at: %s</font>" % formatted_time
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		
		if self.data['type'] == 'productInfo':
			page = self.productInfo()
		if self.data['type'] == 'productTotal':
			page = self.productTotal()
		if self.data['type'] == 'catInfo':
			page = self.catInfo()
		if self.data['type'] == 'catTotal':
			page = self.catTotal()
		if self.data['type'] == 'catTag':
			page = self.catTag()
		if self.data['type'] == 'tagInfo':
			page = self.tagInfo()
		if self.data['type'] == 'tagTotal':
			page = self.tagTotal()
		if self.data['type'] == 'orderInfo':
			page = self.order()
		
		self.doc.build(self.Story)
		
		report = self.buffer.getvalue()
		self.buffer.close()
		
		return report
		
	def productInfo(self):
		ptext = "<font size=6>Bluering Product Report for Barcode: %s</font>" % (self.data['barcode'])
		self.Story.append(Paragraph(ptext, self.styles["leftIndented"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=18>At a glance:</font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 15))
		
		ptext = "<font size=12>Barcode: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		ptext = "<font size=18><b>%s</b></font>" % (self.data['barcode'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=12>Name: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		ptext = "<font size=18><b>%s</b></font>" % (self.data['name'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=12>Quantity: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		ptext = "<font size=18><b>%s</b></font>" % (self.data['quantity'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 24))
		
		ptext = "<font size=18>Additional Information:</font>"
		self.Story.append(Paragraph(ptext, self.styles['Normal']))
		self.Story.append(Spacer(1, 15))
		
		ptext = "<font size=12>Tags: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 2))
		
		ptext = "<font size=12><b>"
		for t in range(len(self.data['tags'])):
			if t == 0:
				ptext += ("%s" % (str(self.data['tags'][t])))
			else:
				ptext += (", %s" % (str(self.data['tags'][t])))
		ptext += "</b></font>"
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 5))
		
		ptext = "<font size=12>Category: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 2))
		
		ptext = "<font size=12><b>%s</b></font>" % (self.data['category'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=12>Description: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 2))
		
		ptext = "<font size=12>%s</font>" % (self.data['description'])
		self.Story.append(Paragraph(ptext, self.styles["leftIndented"]))
		self.Story.append(Spacer(1, 5))
	
	def productTotal(self):
		return None
	
	def catInfo(self):
		return None
	
	def catTotal(self):
		return None
	
	def catTag(self):
		return None
	
	def tagInfo(self):
		return None
		
	def tagTotal(self):
		return None
	
	def order(self):
		self.datum = self.data['data']
		
		ptext = "<font size=6>Bluering Order: %s</font>" % (self.datum['id'])
		self.Story.append(Paragraph(ptext, self.styles["leftIndented"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=18>Order Information:</font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 15))
		
		ptext = "<font size=12>Order Id: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		ptext = "<font size=18><b>%s</b></font>" % (self.datum['id'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 10))
		
		ptext = "<font size=12>User: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		ptext = "<font size=18><b>%s</b></font>" % (self.datum['user'])
		self.Story.append(Paragraph(ptext, self.styles["Blue"]))
		self.Story.append(Spacer(1, 24))
		
		ptext = "<font size=12>Order: </font>"
		self.Story.append(Paragraph(ptext, self.styles["Normal"]))
		self.Story.append(Spacer(1, 6))
		
		
		for t in self.datum['order']:
			ptext = "<font size=14>Barcode: <b>[ %s ]</b></font>" % (t)
			self.Story.append(Paragraph(ptext, self.styles["Blue"]))
			self.Story.append(Spacer(1, 2))
			
			ptext = "<font size=12>Quantity: <b>[ %s ]</b></font>" % (self.datum['order'][t])
			self.Story.append(Paragraph(ptext, self.styles["RedIndent"]))
			self.Story.append(Spacer(1, 5))

		
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