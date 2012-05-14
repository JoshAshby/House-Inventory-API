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

databaseName = 'bluering'
database = couchdbkit.Server()[databaseName]

render = web.template.render('template/')

class slash:
	def GET(self): raise web.seeother("/")
