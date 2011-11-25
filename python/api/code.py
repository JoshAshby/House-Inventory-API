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
from config import *
from configSub import *

#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

app = web.application(urls, globals())
app.internalerror = web.debugerror

class index:        
	'''
	class documentation
	Base Index...
	
	The page that is displayed if the root of the server is accessed, Currently just displays the template index.html
	'''
	
	def endFunc(self):
		print "start"
		raise web.seeother("/product/")
	
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()
		
#app = web.application(urls, globals(), autoreload=False)
#app.internalerror = web.debugerror
#application = app.wsgifunc()
		
		
if __name__ == "__main__":
	print "running"
	app.run()
