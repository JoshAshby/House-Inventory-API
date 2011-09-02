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
import auth

urls = (
	'', 'slash',
	'/(.*)/', 'stats'
)

class stats:
	'''
	class documentation
	
	Generates stats about the given product.
	'''
	def getFunc(self, **kwargs):	
		'''
		function documentation
		
		GET verb call
		
		Returns:
		
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		try:
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		if spam:
			web.header('Content-Type', 'application/json')
		raptor = predict(bar)
		return json.dumps(raptor)
	
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Returns:
		
		'''
		pass
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Returns:
		
		'''
		pass
	
	def deleteFunc(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Returns:
		
		'''
		pass
	
	def GET(self, bar):
		return self.getFunc(barcode=bar)
	
	@auth.oauth_protect
	def POST(self, bar):
		return self.postFunc(barcode=bar)
	
	@auth.oauth_protect
	def PUT(self, bar):
		return self.putFunc(barcode=bar)
	
	@auth.oauth_protect
	def DELETE(self, bar):
		return self.deleteFunc(barcode=bar)
			
		
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
		
	#print len(last_5)
	
	if len(last_5) == 5:
		last_5.pop(0)
	else:
		pass
	
	#print frank[0][0]
	#print last_5
	
	try:
		if frank[0][0] != '':
			try:
				batman = reduce((lambda x, y: x + y), last_5)/5
			except:
				pass
		else:
			batman = 'NED'
			#He's a ninja...
	except:
		batman = 'NED'
	
	#print sara[0]
	#print batman
	
	try:
		spider = sara[0]/batman
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