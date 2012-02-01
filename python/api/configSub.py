#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Sub-App config files and currently the database handlers but those will move soon

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import couchdbkit

databaseName = 'stats'
database = couchdbkit.Server()[databaseName]

render = web.template.render('template/')

debug = 0

'''
firefox debug setter (this is because firefox seems to want to download the json text instead of display it)...
set this to 1 for normal opperation, 0 for firefox...
'''
spam = 0

class slash:
	def GET(self): raise web.seeother("/")

def format(view):
	if 't' in wi: t = wi['t']
	elif 't' in kwargs: t = kwargs['t']
	else: t = 'json'
	
	if t == 'html':
		inform = view.HTML()
	elif t == 'json':
		inform = view.JSON()
	elif t == 'pdf':
		inform = view.PDF()
	return inform