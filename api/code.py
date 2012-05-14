#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API that provides public and admin functions.
Admin calls to the API must be POST and use OAUTH1 2-legged.
This is the main app, which calls upon other sub apps according to whats needed.
This also holds useless test and index classes.

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
from config import *
from configSub import *
import baseObject

baseObject.urlReset()


@baseObject.route('/')
class index(baseObject.baseHTTPObject):  
	'''
	Base Index...
	
	The page that is displayed if the root of the server is accessed, Currently just displays the template index.html
	'''
	def get(self, *args, **kwargs):
		raise web.seeother("product/")


urls += baseObject.urls

app = web.application(urls, globals())
app.internalerror = web.debugerror
		
		
if __name__ == "__main__":
	app.run()
