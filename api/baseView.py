#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Base view prototype

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


class baseView(object):
	def __init__(self, **kwargs):
		self.data = kwargs['data']
		
		self.t = 'json'
		
		if 'wi' in kwargs:
			if 't' in kwargs['wi']: self.t = kwargs['wi']['t']
		
		if self.t == 'html':
			self.inform = self.HTML()
		elif self.t == 'json':
			self.inform = self.JSON()
		elif self.t == 'pdf':
			self.inform = self.PDF()
	
	def PDF(self):
		pass
		
	def HTML(self):
		pass
		
	def JSON(self):
		pass
	
	def returnData(self):
		return self.inform