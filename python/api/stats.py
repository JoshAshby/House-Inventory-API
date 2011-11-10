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
	
	tryal = predict(bar)
	
	if 'error' in tryal:
		return {'barcode': bar, 'error': 'NED'}
	
	replyson = {
		'barcode': bar,
		'rate': tryal['rate'],
		'days': tryal['days']
	}
	
	return replyson
	

def predict(bar):
	query = []
	quantity = []
	date = []
	
	product = productDoc.view("products/admin", key=bar).first()
	
	a = product.log
	
	query = sorted(a, key=lambda a: a['date'], reverse=True)
	
	m = len(query)
	
	dateTime = datetime.datetime.now()

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
		frank.append(polyderiv([sara[d],-bob[d],-math.pow(-bob[d], 2)]))
	
	if frank[len(frank)-1][0]:
		try:
			yoyo = float(sara[1]/frank[1][0])
		except:
			yoyo = 'NED'
	else:
		yoyo = 'NED'

	if yoyo != 'NED':
		spider = sara[1]/yoyo
	else:
		spider = 'NED'
		
	if (str(yoyo)) in product.all:
		product.all[str(yoyo)] += 1
	else:
		product.all[str(yoyo)] = 1
	
	if (str(spider)) in product.allDay:
		product.allDay[str(spider)] += 1
	else:
		product.allDay[str(spider)] = 1
	
	product.predicted['days'] = spider
	product.predicted['rate'] = yoyo
	
	product.save()
	
	#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
	#Ie: Raptor eats everything... nom nom nom
	raptor = {'rate': yoyo, 'days': spider}
	
	return raptor
