#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main admin functions

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import re
import time

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
from ashmath import *
from ashpic import *
import auth
import account

urls = (
	'', 'slash',
	'/(.*)/restore/', 'restore'
)

class restore:
	'''
	class documentation
	Restores a product from the backup database, after that products been deleted.
	
	Returns:
		TODO
	'''
	
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, barcode):
		name = db.query('SELECT * FROM `backup` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		
		db.query('INSERT INTO `products` (`id`, `barcode`, `name`, `description`, `quantity`, `cat`, `tags`, `picture`, `flag`) VALUES ($id, $barcode, $name, $description, $quantity, $cat, $tags, $picture, $flag) ', vars={'barcode': inform['barcode'], 'name': inform['name'], 'quantity':inform['quantity'], 'id': inform['id'], 'description': inform['description'], 'cat': inform['cat'], 'tags': inform['tags'], 'picture': inform['picture'], 'flag': inform['flag']})
		
		alpha = json.loads(inform['log'])
		
		for l in range(len(alpha)):
			beta = alpha[l]['date']
			coi = alpha[l]['quantity']
			db.query('INSERT INTO `usage` (`barcode`, `date`, `quantity`) VALUES ($barcode, $date, $quantity) ', vars={'barcode': inform['barcode'],'date': beta, 'quantity': coi})
		
		db.query('INSERT INTO `stats` (`barcode`, `last_5`, `all`) VALUES ($barcode, $last_5, $all) ', vars={'barcode': inform['barcode'], 'last_5': inform['last_5'], 'all': inform['all']})
		
		
		db.query('DELETE FROM `backup` WHERE `barcode` = $barcode', vars={'barcode': barcode})

		inform['restored'] = 'true'
		inform['log'] = alpha
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()