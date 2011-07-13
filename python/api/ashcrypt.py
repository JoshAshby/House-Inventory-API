#!/usr/bin/env python
"""
Basic password salt and hash class for Project Blue Ring

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
#Don't ask... this error is just better than a standard raise
class CryptError(Exception):
	'''
	class documentation
	CryptError for use with the salt and hash 
	'''
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
class crypt(object):
	def __init__(self, new_salt):
		self.new_salt = new_salt
	
	def saltandpepper(self):
		