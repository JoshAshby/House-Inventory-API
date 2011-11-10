#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Sub-App config files

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import couchdbkit

databaseName = 'stats'

render = web.template.render('template/')

debug = 0

'''
firefox debug setter (this is because firefox seems to want to download the json text instead of display it)...
set this to 1 for normal opperation, 0 for firefox...
'''
spam = 0

class slash:
	def GET(self): raise web.seeother("/")


database = couchdbkit.Server()[databaseName]

class productDoc(couchdbkit.Document):
	barcode = couchdbkit.StringProperty()


class userDoc(couchdbkit.Document):
	username = couchdbkit.StringProperty()


productDoc.set_db(database)
userDoc.set_db(database)
