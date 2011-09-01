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
	'/(.*)/delete/', 'delete',
	'/(.*)/restore/', 'restore',
	'/(.*)/log/', 'log',
	'/(.*)/stats/', 'stats',
	'/category/(.*)/groupstats/', 'catStats',
	'/add/', 'add',
	'/update/', 'update'
)

class slash:
	def GET(self): raise web.seeother("/")

GET_UNAUTHORIZED_MESSAGE = "Your not able to access this from GET and need OAuth to be able to access any of the POST resources for Admins"

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
		
class log:
	'''
	class documentation
	Generates the use log about the given product.
	
	Returns:
		A JSON object like: {"log" : [["2011-03-19 01:15:17", 1], ["2011-02-19 01:15:09", 2], ["2011-02-06 00:47:43", 6], ["2011-02-05 00:47:43", 3]]}
	'''		
	
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, barcode):
		gaia = web.input()
		query = []
		log = []
		name = db.query('SELECT `quantity`, `date` FROM `usage` WHERE `barcode` = $barcode ORDER BY `date` desc', vars={'barcode':barcode})
		for i in range(len(name)):
			query.append(name[i])
		for i in range(len(query)):
			log.append([query[i]['date'].isoformat(' '), query[i]['quantity']])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"log": log})


class stats:
	'''
	class documentation
	Generates stats about the given product.
	
	Returns:
		A JSON object like: {"predicted": -28.0, "rank": 12, "popularity": "Low"}
		
		Where:
			predicted = the predicted rate for when the product will run out, as guessed by the last_5 guesses
			rank = the over all numerical rank of the product.
			popularity = High, Med, Low, or NED
	'''
	
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, barcode):
		if spam:
			web.header('Content-Type', 'application/json')
		raptor = predict(barcode)
		return json.dumps(raptor)

class catStats:
	'''
	class documentation
	Generates stats about the given product.
	
	Returns:
		A JSON object like: {u'3037921120217': {u'popularity': u'High', u'predicted': u'NED', u'rank': 2}, u'043396366268': {u'popularity': u'Med', u'predicted': -35.0, u'rank': 3}, u'dog987': {u'popularity': u'High', u'predicted': -1.25, u'rank': 1}}
		
		Where:
			predicted = the predicted rate for when the product will run out, as guessed by the last_5 guesses
			rank = the over all numerical rank of the product.
			popularity = High, Med, Low, or NED
	'''
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, category):
		query = []
		name = db.query('SELECT `barcode` FROM `products` WHERE `cat` = $cat', vars = {'cat': category})
		
		for i in range(len(name)):
			query.append(name[i])
		
		raptop = {}
		
		for dino in range(len(query)):
			raptop[query[dino]['barcode']] = predict(query[dino]['barcode'])
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(raptop)
		
def predict(barcode):
	query = []
	quantity = []
	date = []
	
	name = db.query('SELECT `quantity`, `date` FROM `usage` WHERE `barcode` = $barcode ORDER BY `date` desc', vars={'barcode':barcode})
	
	for i in range(len(name)):
		query.append(name[i])
	
	m = len(query)
	
	#Here we have to get all the data points from the stats database (usage) so we can do fancy things to get some nice predictions.
	for i in range(m):
		if (i+1) == m:
			quantity.append(float(query[i]['quantity']))
			date.append(float((query[0]['date'] - query[i]['date']).days))
			break
		elif (query[i]['quantity'] < query[i+1]['quantity']):
			quantity.append(float(query[i]['quantity']))
			date.append(float((query[0]['date'] - query[i]['date']).days))
		else:
			quantity.append(float(query[i]['quantity']))
			date.append(float((query[0]['date'] - query[i]['date']).days))
			break
	
	#its 2am and I got bored with standard naming conventions...
	bob = thorVector(date)
	sara = thorVector(quantity)
	frank = thorVector([])
	raven = []
	
	#take the partial deriv of each part of the vector to gain the total deriv or gradient...
	for d in range(len(bob)):
		frank.append(polyderiv([sara[d],-bob[d],-bob[d]**2]))
	
	stat  = db.query('SELECT `last_5`, `all` FROM `stats` WHERE `barcode` = $barcode', vars={'barcode':barcode})
	
	for q in range(len(stat)):
		raven.append(stat[q])
	
	try:
		last_5Raw = raven[0]['last_5']
	except:
		lasat_5Raw = []
		
	try:
		allRaw = raven[0]['all']
	except:
		allRaw = []
	
	try:
		last_5 = json.loads(last_5Raw)
	except:
		last_5 = []
	
	try:
		all = json.loads(allRaw)
	except:
		all = []
	
	try:
		if len(last_5) == 5:
			last_5.pop(0)
		else:
			pass
	except:
		pass
	
	try:
		if frank[1][0]:
			try:
				batman = reduce((lambda x, y: x + y), last_5)/5
			except:
				pass
		else:
			batman = 'NED'
			#He's a ninja...
	except:
		batman = 'NED'
	
	try:
		spider = sara[1]/batman
	#	spider = 'NED'
	except:
		spider = 'NED'
	
	#and now I have the hic-ups...
	db.query('UPDATE `stats` SET `last_5` = $last_5, `all` = $all WHERE `barcode` = $barcode', vars={'last_5': json.dumps(last_5), 'all': json.dumps(all) , 'barcode': barcode})
	
	blowing = []
	soda = 5
	
	bubble = db.query('SELECT `barcode`, `last_5` FROM `stats`')
	
	for q in range(len(bubble)):
		blowing.append(bubble[q])
		
	#insert programming joke here....
	bubble_sort = sorted(blowing, key=lambda bubbles: bubbles['last_5'][0])
	
	for h in range(len(bubble_sort)):
		bubble_sort[h]['rank'] = h
	
	for k in range(len(bubble_sort)):
		if bubble_sort[k]['barcode'] == str(barcode):
			soda = bubble_sort[k]['rank']
	
	pop = float(soda)/float(len(bubble_sort))
	
	ran = (float(bubble_sort[len(bubble_sort)-1]['rank'])/float(len(bubble_sort)))/3
	
	'''
	Next we'll go through and set the flag for the called product, this again may later be the flags for the whole product group
	so that even if a product hasn't been checked in years and years for popularity (it just isn't popular I guess) it will still have updated
	stats. 
	'''
	if pop <= ran:
		ger = 'High'
		flag = 'H'
		db.query("UPDATE `products` SET `flag` = $flag WHERE `barcode` = $barcode",vars={'flag': flag, 'barcode': barcode})
	elif pop <= (ran*2):
		ger = 'Med'
		flag = 'M'
		db.query("UPDATE `products` SET `flag` = $flag WHERE `barcode` = $barcode",vars={'flag': flag, 'barcode': barcode})
	elif pop >= (ran*2):
		ger = 'Low'
		flag = 'L'
		db.query("UPDATE `products` SET `flag` = $flag WHERE `barcode` = $barcode",vars={'flag': flag, 'barcode': barcode})
	else:
		ger = 'NED'
		flag = 'L'
		db.query("UPDATE `products` SET `flag` = $flag WHERE `barcode` = $barcode",vars={'flag': flag, 'barcode': barcode})
	
	#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
	#Ie: Raptor eats everything... nom nom nom
	raptor = {'predicted': spider, 'rank': soda, 'popularity': ger}
	
	return raptor


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()