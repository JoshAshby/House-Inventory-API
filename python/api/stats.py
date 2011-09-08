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
import json
import re
import time
import math
from datetime import datetime

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

def stat(bar):
	query=[]
	
	name = db.select('stats', where='barcode=$barcode', vars={'barcode': bar}, _test=False)

	for i in range(len(name)):
		query.append(name[i])
	
	#all = json.loads(query[0]['all'])
	#last_5 = json.loads(query[0]['last_5'])
	dataRaw = json.loads(query[0]['data'])
	all = dataRaw['all']
	last_5 = dataRaw['last5']
	allDay = dataRaw['allDay']
	last5Day = dataRaw['last5Day']
	setAllDay = list(set(allDay))
	lengDay = len(setAllDay)
	set_all = list(set(all))
	leng = len(set_all)
	
	ans = predict(bar, 1)
	rankPro = json.loads(rank(bar))
	
	#
	added = 0
	for q in range(leng):
		added += set_all[q]
		
	avg = added/(leng)
	
	prestd = 0
	for s in range(leng):
		setr = math.pow((set_all[s] - avg), 2)
		prestd += setr
	
	stddv = math.sqrt(prestd/leng)
	
	#now days instead of rates
	added = 0
	for q in range(lengDay):
		added += setAllDay[q]
		
	avg = added/(leng)
	
	prestd = 0
	for s in range(lengDay):
		setr = math.pow((setAllDay[s] - avg), 2)
		prestd += setr
	
	stddvDay = math.sqrt(prestd/lengDay)
	
	reply = {
		'barcode': bar,
		'stddv': stddv,
		'stddvDay': stddvDay,
		'guess': ans['guess'],
		'predicted': ans['predicted'],
		'rank': rankPro['rank'],
		'last5': last_5,
		'all': all,
		'last5Day': last5Day,
		'allDay': allDay
	}
	
	try:
		product = productDoc(barcode=bar).get(bar)
	except:
		product = productDoc(barcode=bar)
		
	product.stddv = reply['stddv']
	product.guess = reply['guess']
	product.predicted = reply['predicted']
	product.stddvDay = reply['stddvDay']
	product.last5 = reply['last5']
	product.last5Day = reply['last5Day']
	product.all = reply['all']
	product.allDay = reply['allDay']
	product.rank = reply['rank']
	
	product._id = bar
	product.save()
	
	replyson = {
		'barcode': bar,
		'guess': ans['guess'],
		'predicted': ans['predicted'],
		'rank': rankPro['rank']
	}
	
	return replyson
	

def predict(barcode, zombie):
	query = []
	quantity = []
	date = []
	
	name = db.query('SELECT `quantity`, `date` FROM `usage` WHERE `barcode` = $barcode ORDER BY `date` desc', vars={'barcode':barcode})
	
	for i in range(len(name)):
		query.append(name[i])
	
	m = len(query)
	
	#Here we have to get all the data points from the stats database (usage) so we can do fancy things to get some nice predictions.
	if zombie:
		for i in range(m):
			if (i+1) == m:
				quantity.append(float(query[i]['quantity']))
				date.append(float((datetime.now() - query[i]['date']).days))
				break
			elif (query[i]['quantity'] > query[i+1]['quantity']):
				quantity.append(float(query[i]['quantity']))
				date.append(float((datetime.now() - query[i]['date']).days))
				break
			else:
				quantity.append(float(query[i]['quantity']))
				date.append(float((datetime.now() - query[i]['date']).days))
	else:
		for i in range(m):
			if (i+1) == m:
				quantity.append(float(query[i]['quantity']))
				date.append(float((query[0]['date'] - query[i]['date']).days))
				break
			elif (query[i]['quantity'] > query[i+1]['quantity']):
				quantity.append(float(query[i]['quantity']))
				date.append(float((query[0]['date'] - query[i]['date']).days))
				break
			else:
				quantity.append(float(query[i]['quantity']))
				date.append(float((query[0]['date'] - query[i]['date']).days))
	
	#its 2am and I got bored with standard naming conventions...
	bob = thorVector(date)
	sara = thorVector(quantity)
	frank = thorVector([])
	raven = []
	
	#take the partial deriv of each part of the vector to gain the total deriv or gradient...
	for d in range(len(bob)):
		frank.append(polyderiv([sara[d],-bob[d],math.pow(-bob[d], 2)]))
	
	if frank[len(frank)-1][0]:
		yoyo = sara[1]/frank[1][0]
	else:
		yoyo = 'NED'

	'''
	These next few lines go through and do the rolling list and total rates for the product
	rates are the intercepts of the gradient.
	These rates are stored in the database table 'stats' and are stored as json objects for ease of use and storage.
	'''
	
	#load the stats info
	stat  = db.query('SELECT `last_5`, `all`, `data` FROM `stats` WHERE `barcode` = $barcode', vars={'barcode':barcode})
	
	#error prevention stuff...
	for q in range(len(stat)):
		raven.append(stat[q])
	
	try:
		dataRaw = json.loads(raven[0]['data'])
	except:
		pass
	
	try:
		#last_5Raw = raven[0]['last_5']
		last_5 = dataRaw['last5']
	except:
		#last_5Raw = []
		last_5= []
		
	try:
		#allRaw = raven[0]['all']
		all = dataRaw['all']
	except:
		#allRaw = []
		all = []

	#last_5 = json.loads(last_5Raw)

	#all = json.loads(allRaw)

	if len(last_5) == 5:
		last_5.pop(0)
	else:
		pass

	if yoyo != 'NED':
		last_5.append(yoyo)
		all.append(yoyo)
		
	try:
		batman = reduce((lambda x, y: x + y), last_5)/5
	except:
		#He's a ninja...
		batman = 'NED'

	if batman != 'NED':
		spider = sara[1]/batman
		intSpider = int(spider)
	else:
		spider = 'NED'
		intSpider = 'NED'

	#and now I have the hic-ups...
	try:
		current = frank[1][0]
	except:
		current = 'NED'
	
	try:
		allDay = dataRaw['allDay']
	except:
		allDay = []
	allDay.append(intSpider)
	
	try:
		lastDay = dataRaw['last5Day']
	except:
		lastDay = []
	
	if len(lastDay) == 5:
		lastDay.pop(0)
	else:
		pass
	
	lastDay.append(intSpider)
	
	dat = {'day': intSpider, 'allDay': allDay, 'last5Day': lastDay, 'all': all, 'last5': last_5}
	
	db.query('UPDATE `stats` SET `last_5` = $last_5, `all` = $all, `data` = $data WHERE `barcode` = $barcode', vars={'last_5': json.dumps(last_5), 'all': json.dumps(all) , 'barcode': barcode, 'data': json.dumps(dat)})

	#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
	#Ie: Raptor eats everything... nom nom nom
	#raptor = {'current': current, 'standard':  yoyo, 'guess': batman, 'predicted': spider, 'predictedNF': intSpider}
	#raptor = {'predicted': spider, 'rank': soda, 'popularity': ger}
	raptor = {'guess': batman, 'predicted': intSpider}
	
	return raptor


def rank(barcode):
	#these next few lines set up the rank to the rest of the products.
	blowing = []
	soda = 5
	
	bubble = db.query('SELECT `barcode`, `last_5`, `data` FROM `stats`')
	
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
	
	raptop = {'rank': soda, 'popularity': ger}
	return json.dumps(raptop)