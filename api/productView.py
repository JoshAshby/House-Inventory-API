#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Product information views

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
import baseView


class infoView(baseView.baseView):
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({'product': self.data['value']})
		
	def HTML(self):
		self.data['type'] = 'productInfo'
		prePage = htmlView(self.data['value'])
		page = prePage.build()
		
		web.header('Content-Type', "text/html")
		
		return page


class totalView(baseView.baseView):
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"total": self.data['data']})

class errorView(baseView.baseView):
	def JSON(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"error": self.data['error'], 'missing': self.data['missing']})