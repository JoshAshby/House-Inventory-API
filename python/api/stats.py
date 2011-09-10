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
#from datetime import datetime
import datetime

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
	
	predict(bar, 1)
	rank(bar)
	
	dataRaw = database.view("products/admin", key=bar).first()['value']
	
	replyson = {
		'barcode': bar,
		'guess': dataRaw['predicted']['rate'],
		'predicted': dataRaw['predicted']['days'],
		'rank': dataRaw['rank']
	}
	
	return replyson
	

def predict(bar, zombie):
	query = []
	quantity = []
	date = []
		
	a = database.get(bar)['log']
	
	query = sorted(a, key=lambda a: a['date'], reverse=True)
	
	m = len(query)
	
	#Here we have to get all the data points from the stats database (usage) so we can do fancy things to get some nice predictions.
	if zombie:
		dateTime = datetime.datetime.now() 
	else:
		dateTime = datetime.datetime.strptime(query[0]['date'], '%Y-%m-%d %H:%M:%S')
		
	for i in range(m):
		if (i+1) == m:
			quantity.append(float(query[i]['quantity']))
			date.append(float((dateTime - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
			break
		elif (query[i]['quantity'] > query[i+1]['quantity']):
			quantity.append(float(query[i]['quantity']))
			date.append(float((dateTime - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
			break
		else:
			quantity.append(float(query[i]['quantity']))
			date.append(float((dateTime - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
	
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
	
	last_5 = database.get(bar)['last5']
	
	try:
		batman = reduce((lambda x, y: x + y), last_5)/5
	except:
		#He's a ninja...
		batman = 'NED'

	if batman != 'NED':
		spider = sara[1]/batman
		intSpider = int(spider)
	else:
		intSpider = 'NED'
	
	#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
	#Ie: Raptor eats everything... nom nom nom
	#raptor = {'current': current, 'standard':  yoyo, 'guess': batman, 'predicted': spider, 'predictedNF': intSpider}
	#raptor = {'predicted': spider, 'rank': soda, 'popularity': ger}
	raptor = {'guess': batman, 'predicted': intSpider}
	
	return raptor


def rank(barcode):
	#these next few lines set up the rank to the rest of the products.
	blowing = []
	soda = 0
	
	blowing = database.view("products/admin").all()
		
	#insert programming joke here....
	bubble_sort = sorted(blowing, key=lambda bubbles: bubbles['value']['last5'][0])
	
	for h in range(len(bubble_sort)):
		bubble_sort[h]['value']['rank'] = h
	
	for k in range(len(bubble_sort)):
		if bubble_sort[k]['value']['barcode'] == str(barcode):
			soda = bubble_sort[k]['value']['rank']
	
	pop = float(soda)/float(len(bubble_sort))
	
	ran = (float(bubble_sort[len(bubble_sort)-1]['value']['rank'])/float(len(bubble_sort)))/3
	
	'''
	Next we'll go through and set the flag for the called product, this again may later be the flags for the whole product group
	so that even if a product hasn't been checked in years and years for popularity (it just isn't popular I guess) it will still have updated
	stats. 
	'''
	pro = productDoc.get(barcode)
	if pop <= ran:
		ger = 'High'
		flag = 'H'
		pro.flag = flag
	elif pop <= (ran*2):
		ger = 'Med'
		flag = 'M'
		pro.flag = flag
	elif pop >= (ran*2):
		ger = 'Low'
		flag = 'L'
		pro.flag = flag
	else:
		ger = 'NED'
		flag = 'L'
		pro.flag = flag
	
	raptop = {'rank': soda, 'popularity': ger}
	return json.dumps(raptop)