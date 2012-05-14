#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
HTML design view object

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

from Cheetah.Template import Template

class htmlView(object):
	def __init__(self, data):
		self.data = data
	
	def build(self):
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
		
		return page
		
	def productInfo(self):
		page = Template(file="template/info.html", searchList=[self.data])
		
		return page
	
	def productTotal(self):
		page = Template(file="template/total.html", searchList=[{"data": self.data['data'], "title": "<b>Total Inventory</b>", 'type': 'Total Inventory'}])
		
		return page
	
	def catInfo(self):
		page = Template(file="template/total.html", searchList=[{"data": self.data['data'], "title": ("<b>Category:</b>" + self.data['data'][0]['category']), 'type': self.data['data'][0]['category']}])
		
		return page
	
	def catTotal(self):
		page = Template(file="template/cats.html", searchList=[{"data": self.data['data'], "title": "<b>Categories</b>", 'type': 'category'}])
		
		return page
	
	def catTag(self):
		page = Template(file="template/total.html", searchList=[{"data": self.data['data'], "title": ("<b>Category:</b> "+self.data['data'][0]['category'] + "<b> Tag: </b>" + self.data['tag']), 'type': (self.data['data'][0]['category'] + " " + self.data['tag'])}])
		
		return page
	
	def tagInfo(self):
		page = Template(file="template/total.html", searchList=[{'data': self.data['data'], "title": ("<b>Tag: </b>" + self.data['tag']), 'type': self.data['tag']}])
		
		return page
		
	def tagTotal(self):
		page = Template(file="template/cats.html", searchList=[{"data": self.data['data'], "title": "<b>Tags</b>", 'type': 'tag'}])
		
		return page
	
	def order(self):
		page = Template(file="template/order.html", searchList=[{"data": self.data['data']}])
		
		return page