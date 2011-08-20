#!/usr/bin/env python
"""
Project Blue Ring
A scalable inventory control and management system based in the cloud.
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
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from config import *

USERERROR_MESSAGE = "There was a error with the USER"
USERNO_MESSAGE = "The user and password do not match anyone in the database..."

class account:
	def findByKey(self, key):
		alpha = db.select('pepper', where="shared=$key", limit=1, _test=False, vars = {'key': key})
		if not alpha:
			raise web.unauthorized( USERERROR_MESSAGE )
		beta = alpha[0]
		return {'secret': beta['secret'], 'shared': beta['shared'], 'user': beta['user'], 'passwd': beta['passwd'], 'data': beta['data']}
		
	def findByUser(self, user):
		alpha = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': user})
		if not alpha:
			raise web.unauthorized( USERERROR_MESSAGE )
		beta = alpha[0]
		return {'secret': beta['secret'], 'shared': beta['shared'], 'user': beta['user'], 'passwd': beta['passwd'], 'data': beta['data']}
		
	def delete(self, user):
		egg = ''
		if user['user']:
			egg=user['user']
		elif user['key']:
			egg=user['key']
		try:
			zygot = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': egg})
		except:
			zygot = db.select('pepper', where="shared=$key", limit=1, _test=False, vars = {'key': egg})
		phoenix = zygot[0]
		print db.insert('salt', user=phoenix['user'], passwd=phoenix['passwd'], secret=phoenix['secret'], shared=phoenix['shared'], data=phoenix['data'], _test=True)
		#db.delete()
		
	def update(self, data):
		#db.select(
		#db.update()
		pass
		
	def add(self, data):
		#acc['shared'] = ''.join( random.choice(string.letters) for i in xrange(32) )
		#acc['secret'] = ''.join( random.choice(string.letters) for i in xrange(32) )
		pass
		
	def login(self, data):
		yepno = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': data['user']})
		yn = yepno[0]
		if not yn:
			web.unauthorized( USERNO_MESSAGE )
		if yn['passwd'] != data['passwd']:
			web.unauthorized( USERNO_MESSAGE )
		zygot = {}
		zygot['time']=str(int(time.time()))
		zygot['ip']=web.ctx.ip
		egg = json.dumps(zygot)
		db.update('pepper', where="user=$user", _test=False, vars={'user':data['user']}, data=egg)
		return {'status': 'success'}
		'''for key, value in zygot:
			value = str(value)
			web.ctx.session[ key ] = ( value[:50] + '...' ) if len(value) > 50 else value'''