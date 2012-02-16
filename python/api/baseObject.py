#!/usr/bin/env python2
"""
{Web: PyTe}
A capstone project by Josh Ashby, 2011-2012
Base objects which are used for HTTPObjects and a automatic router decorator

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import json
import web
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

urls = (
	"", "slash"
)

def urlReset():
	global urls
	urls = (
		"", "slash"
	)

def route(routeURL):
	"""
	Automatic route decorator
	
	Auto adds the decorated object to the url routing pool
	
	Usage:
		@route("/(.*)/")
	"""
	def wrapper(HTTPObject):
		global urls
		urls += (routeURL, HTTPObject.__name__,)
		return HTTPObject
	return wrapper

class baseHTTPObject(object):
	"""
	Base HTTP Object which provides a setup that is capable of being used as a
	module through the *Func calls, and usable as a web.py Object through the
	GET/POST/PUT/DELETE calls.
	
	Simply inherit this object and over ride get/post/put/delete (lower case)
	with your code.
	"""
	def get(self, *args, **kwargs):
		pass
	
	def post(self, *args, **kwargs):
		pass
	
	def put(self, *args, **kwargs):
		pass
	
	def delete(self, *args, **kwargs):
		pass
	
	def GET(self, *args, **kwargs):
		print args
		return self.get(*args, **kwargs)
	
	def POST(self, *args, **kwargs):
		return self.post(*args, **kwargs)
	
	def PUT(self, *args, **kwargs):
		return self.put(*args, **kwargs)
	
	def DELETE(self, *args, **kwargs):
		return self.delete(*args, **kwargs)
	
	def members(self, *args, **kwargs):
		'''
		'''
		self.sentArgs = args[0].split('/')
		self.sentKwargs = kwargs

	def hasMember(self, tag, none=None):
		'''
		Looks through the args and kwargs for the given tag.
		
		If no tag match is found, reply is arg[0]
		
		Accepts:
			tag - the given tag for data which to look for, or the argument number to return
			
			none - whether this returns None or args[0]
		
		Returns:
			
		'''
		if type(tag) is str:
			wi = web.input(picture={})
			if tag in wi: return wi[tag]
			elif tag in self.sentKwargs: return self.sentKwargs[tag]
			else:
				if none is None: return self.sentArgs[0]
				else: return None
		else:
			return self.sentArgs[int(tag)]