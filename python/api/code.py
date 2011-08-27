#!/usr/bin/env python
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
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from config import *
from configSub import *

"""
Fancy TODO list:
public Tag function that returns something like {"tags": ["a", "b"]}
admin Tag function to add or remove or edit a tag
admin category Stats function that is like the normal admin.py stats however calls it for every product
clean up admin.py Stats function
make tag.py; sort of like cat.py but with tags instead. This way products can be grouped even better, you can look at a 
	category but then also look at the tags within that category to really refine the search
make a search function/search.py
"""

class index:        
	'''
	class documentation
	Base Index...
	
	The page that is displayed if the root of the server is accessed, Currently just displays the template index.html
	'''
	
	def endFunc(self):
		return render.index()
	
	def GET(self):
		return self.endFunc()
		
	def POST(self):
		return self.endFunc()
		
		
if __name__ == "__main__":
	app.run()

#wsgi stuff
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()