#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
User Account info retriver for use with auth.py

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import time
import json
'''
From: http://webpy.org/install and http://code.google.com/p/modwsgi/wiki/ApplicationIssues
This must be done to avoid the import errors which come up with having linear.py and config.py
'''
try:
	from configSub import *
	import os, sys
except:
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
import couchdbkit
import hashlib
import datetime

USERERROR_MESSAGE = "There was a error with the username or password"

class account:
	def findUser(self, keyer, type=''):
		if type is 'username':
			alpha = "admin/user"
		elif type is 'key':
			alpha = "admin/all"
		else:
			alpha = "admin/user"
	
		beta = database.view(alpha, key=keyer).first()['value']
		
		if not beta:
			raise web.unauthorized( USERERROR_MESSAGE )
			
		return {'secret': beta['oauth']['secret'], 'shared': beta['oauth']['shared'], 'username': beta['username'], 'password': beta['password'], 'logged_in': beta['logged_in'], 'ip': beta['ip'], 'datetime': beta['datetime']}
	
	def addUser(self, **kwargs):
		new = userDoc(username=kwargs['name'])
		
		saltdb = ''.join(map(lambda x:'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[ord(x)%64], os.urandom(16)))
		new.salt = saltdb
		
		new.password = kwargs['passwd']
		
		hashed = hashlib.sha512(kwargs['passwd']+saltdb).hexdigest()
		new.hash = hashed
		
		new.email = kwargs['email']
		
		if 'permission' in kwargs: new.permission = kwargs['permission']
		else: new.permission = 'subscriber'
		
		new.save()
		
		reply = {
			"user": kwargs['name'],
			"added": 'true',
			"hash": hashed
		}
		
		return reply
	
	def loginPass(self, user, passed):
		a = database.view("admin/user", key=user).first()['value']

		passwd = str(a['password'])
		saltwd = str(a['salt'])

		#b = hashlib.sha512(passwd+saltwd).hexdigest()
		b = str(a['hash'])
		c = hashlib.sha512(passed+saltwd).hexdigest()

		if b == c:
			use = userDoc.get(a['_id'])
			use.logged_in = 'true'
			use.datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
			try:
				use.ip = web.ctx.ip.get()
			except:
				use.ip = '::1'
			
			use.save()
			
			reply = {
				"username": user,
				"logged_in": "true"
			}
			
			return reply
		else: raise web.unauthorized( USERERROR_MESSAGE )
		
	def loginHash(self, user, hash):
		a = database.view("admin/user", key=user).first()['value']

		passwd = str(a['password'])
		saltwd = str(a['salt'])

		c = hashlib.sha512(passwd+saltwd).hexdigest()

		if hash == c:
			use = userDoc.get(a['_id'])
			use.logged_in = 'true'
			use.datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
			try:
				use.ip = web.ctx.ip.get()
			except:
				use.ip = '::1'
			
			use.save()
			
			reply = {
				"username": user,
				"logged_in": "true"
			}
			
			return reply
		else: raise web.unauthorized( USERERROR_MESSAGE )
	
	def logout(self, user):
		a = database.view("admin/user", key=user).first()['value']['_id']
		use = userDoc.get(a)
		
		use.logged_in = 'false'
		use.save()
		
		reply = {
			"username": user,
			"logged_in": "false"
		}
		
		return reply
	
	def isLoged(self, user):
		a = database.view("admin/user", key=user).first()['value']['logged_in']
		if a == 'true':
			return True
		else:
			return False
	
	def reset(self, user):
		a = database.view("admin/user", key=user).first()['value']['_id']
		new = userDoc.get(a)
		
		saltdb = ''.join(map(lambda x:'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[ord(x)%64], os.urandom(16)))
		new.salt = saltdb
		
		passwd = ''.join(map(lambda x:'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[ord(x)%64], os.urandom(16)))
		new.password = passwd
		
		hashed = hashlib.sha512(passwd+saltdb).hexdigest()
		new.hash = hashed
		
		new.save()
		
		reply = {
			"username": user,
			"temp_password": passwd,
			"temp_hash": hashed
		}
		
		return reply
	
	def update(self, user, **kwargs):
		a = database.view("admin/user", key=user).first()['value']['_id']
		new = userDoc.get(a)
		
		if 'passwd' in kwargs:
			saltdb = ''.join(map(lambda x:'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[ord(x)%64], os.urandom(16)))
			new.salt = saltdb
			
			new.password = kwargs['passwd']
		
			hashed = hashlib.sha512(kwargs['passwd']+saltdb).hexdigest()
			new.hash = hashed
		
		if 'email' in kwargs: new.email = kwargs['email']
		if 'permission' in kwargs: new.permission = kwargs['permission']
		if 'name' in kwargs: new.username = kwargs['name']
		
		new.save()
		
		reply = {
			"username": user,
			"updated": 'true'
		}
		
		return reply
	
	def delete(self, user):
		a = database.view("admin/user", key=user).first()['value']['_id']
		database.delete_doc(a)
		
		reply = {
			"username": user,
			"deleted": 'true'
		}
		
		return reply