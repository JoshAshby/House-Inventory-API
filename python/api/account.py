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
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *

USERERROR_MESSAGE = "There was a error with the USER"
USERNO_MESSAGE = "The user and password do not match anyone in the database..."

class account:
	def findByKey(self, key):
		alpha = db.select('pepper', where="shared=$key", limit=1, _test=False, vars = {'key': key})
		if not alpha:
			print "bettle"
			raise web.unauthorized( USERERROR_MESSAGE )
		beta = alpha[0]
		return {'secret': beta['secret'], 'shared': beta['shared'], 'user': beta['user'], 'passwd': beta['passwd'], 'data': beta['data']}
		
	def findByUser(self, user):
		alpha = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': user})
		if not alpha:
			print "worst"
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
			print "yes"
			raise web.unauthorized( USERNO_MESSAGE )
		if yn['passwd'] != data['passwd']:
			print "think again"
			raise web.unauthorized( USERNO_MESSAGE )
		zygot = {}
		zygot['time']=str(int(time.time()))
		zygot['ip']=web.ctx.ip
		zygot['logged']='true'
		egg = json.dumps(zygot)
		db.update('pepper', where="user=$user", _test=False, vars={'user':data['user']}, data=egg)
		return {'status': 'success'}
	
	def isLoggedIn(self, user):
		yes = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': user})
		no =yes[0]
		tester = json.loads(no['data'])
		if tester['logged'] == "false":
			b = login({'user': tester['user'], 'passwd': tester['passwd']})
			return b
		return {'logged': tester['logged']}
	
	def logout(self, user):
		'''
		Not currently used in this API right now...
		'''
		yepno = db.select('pepper', where="user=$user", limit=1, _test=False, vars = {'user': user})
		yn = yepno[0]
		if not yn:
			print "No such user..."
			return {'status': 'failed'}
		zygot = {}
		zygot['time']=yn['time']
		zygot['ip']=yn['ip']
		zygot['logged']='false'
		egg = json.dumps(zygot)
		db.update('pepper', where="user=$user", _test=False, vars={'user':data['user']}, data=egg)
		return {'status': 'success'}