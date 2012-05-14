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
import json
import web
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *


urls = (
	'', 'slash'
)


def urlReset():
	'''
	Resets the url pool, must be called at the start of a new file if @route is being used in that file
	'''
	global urls
	urls = (
		'','slash'
	)


def route(routeURL):
	"""
	Automatic route generation decorator
	
	Auto adds the decorated object to the url routing pool
	
	Usage:
		@route("/(.*)/")
		or @baseObject.route("/(.*)/")
		
		where "/(.*)/" is the routing regex
		
		and in the object, replace urls with baseObject.urls or
		urls += baseObject.urls
		to use this module.
	"""
	def wrapper(HTTPObject):
		global urls
		urls += (routeURL, HTTPObject.__name__,)
		return HTTPObject
	return wrapper


class baseHTTPObject(object):
	"""
	Base HTTP Object which provides a setup that is capable of being used as a
		module for testing through the lowercase get/post/put/delete calls,
		and usable as a web.py Object through the GET/POST/PUT/DELETE calls.
	
	Simply inherit this object and over-ride get/post/put/delete (lower case)
		with your code.
	
	Then to get a variable, use self.hasMember(tag) where tag is either the argument number
		or the keyword for: kwargs or web.input.
	
	get/post/put/delete can be called with api urls like so:
		/1
		/1/
		/?file=1
	
	This ensures that the API is accessable from almost every type of calling scheme out there,
		or GET/POST/PUT/DELETE can be imported into a test script, and passed either a argument,
		keyworded argument according to what the object is looking for,
		or web.request() could be used with paste to make a web.input() object
		to use in the test. This makes the object as flexible as possible for both the actual
		web framework or unit tests.
	"""
	def get(self):
		pass
	
	def post(self):
		pass
	
	def put(self):
		pass
	
	def delete(self):
		pass
	
	def GET(self, *args, **kwargs):
		self.members(*args, **kwargs)
		return self.get()
	
	def POST(self, *args, **kwargs):
		self.members(*args, **kwargs)
		return self.post()
	
	def PUT(self, *args, **kwargs):
		self.members(*args, **kwargs)
		return self.put()
	
	def DELETE(self, *args, **kwargs):
		self.members(*args, **kwargs)
		return self.delete()
	
	def members(self, *args, **kwargs):
		'''
		Builds the argument and kwargs list to search through with hasMember
		'''
		try:
			if args[0]:
				firstArgs = args[0].split('/')
				firstArgs.extend(args)
				self.sentArgs = firstArgs
		except:
			self.sentArgs = args
		self.sentKwargs = kwargs

	def hasMember(self, tag, none=None):
		'''
		Looks through the args and kwargs for the given tag.
		
		If no tag match is found, reply is arg[0]
		
		Args:
			tag - the given tag for data which to look for, or the argument number to return
			
			none - whether this returns None or args[0]
		
		Returns:
			Either:
				The given tag's value
				None if none is set to None, and the tag can not be found
				or arg[0] if none is not set to None
		'''
		if type(tag) is str:
			wi = web.input(picture={})
			if tag in wi:
				return wi[tag]
			if tag in self.sentKwargs:
				return self.sentKwargs[tag]
			
			if none is None:
				return self.sentArgs[0]
			return None
		
		if type(tag) is int:
			return self.sentArgs[int(tag)]