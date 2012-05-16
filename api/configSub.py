#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Sub-App config files and currently the database handlers but those will move soon

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import couchdbkit

'''
Set this to either:
	gevent
or
	web.py
	
To determine the underlying wsgi server for the application.
If set to gevent, be sure to also change HTTPport to the port
you want to server the main HTTP interface on.
'''
serverType = 'gevent'

HTTPport = 80

databaseName = 'stats'
database = couchdbkit.Server()[databaseName]

render = web.template.render('template/')

class slash:
	def GET(self): raise web.seeother("/")
