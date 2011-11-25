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

from Cheetah.Template import Template

from reportlab.platypus import *

class infoView(object):
	def __init__(self, data):
		self.data = data
	
	def PDF(self):
		pass
		
	def HTML(self):
		page = Template(file="template/total.html", searchList=[{"data": self.data, "title": ("<b>Category:</b>" + self.data[0]['category']), 'type': self.data[0]['category']}])
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({'products': self.data})

class totalView(object):
	def __init__(self, data):
		self.data = data
	
	def PDF(self):
		pass
		
	def HTML(self):
		print self.data
		page = Template(file="template/cats.html", searchList=[{"data": self.data, "title": "<b>Categories</b>", 'type': 'category'}])
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"categories": self.data})
		
class tagView(object):
	def __init__(self, data, tag):
		self.data = data
		self.tag = tag
	
	def PDF(self):
		pass
		
	def HTML(self):
		print self.data
		page = Template(file="template/total.html", searchList=[{"data": self.data, "title": ("<b>Category:</b> "+self.data[0]['category'] + "<b> Tag: </b>" + self.tag), 'type': (sellf.data[0]['category'] + " " + self.tag)}])
		web.header('Content-Type', "text/html")
		return page
		
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"products": self.data})