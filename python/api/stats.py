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

def restock(bar, restockQuantity):
	f = open("/tmp/statsCalled", "wr")
	f.write("True")
	f.close()
	#try to predict the when the current quantity will run out. The data this saves to the database 
	#is then used later in gradient but needs to ran now before the log and quantity of the product 
	#are updated since it looks at the last peak
	predict(bar)
	
	#pull the products database and copy it into a local variable
	product = productDoc.view("products/admin", key=bar).first()
	
	a = product.log
	
	#sort the log to make sure it's in order, incase some products get out of order somehow.
	query = sorted(a, key=lambda a: a['date'], reverse=True)
	
	dateTimeNow = datetime.datetime.now()
	dateTimeLast = datetime.datetime.strptime(query[0]['date'], '%Y-%m-%d %H:%M:%S')
	
	#calculate the difference between now and the last time the quantity changed, ie: the time
	#it took for the product to reach zero. Then store the correct values in the database
	correctDay = float((dateTimeNow - dateTimeLast).days)
	
	if str(correctDay) in product.allCorrectDay:
		product.allCorrectDay[str(correctDay)] += 1
	else:
		product.allCorrectDay[str(correctDay)] = 1
	
	#calculate the correctRate by taking the current quantity and dividing it by the number of days it took to reach zero
	#then store it in the bucket list for furture needs
	correctRate = float(int(product.quantity)/correctDay)
	
	#store the current correct values for easy access in gradient()
	product.correct['rate'] = correctRate
	product.correct['days'] = correctDay
	
	if str(correctRate) in product.allCorrectRate:
		product.allCorrectRate[str(correctRate)] += 1
	else:
		product.allCorrectRate[str(correctRate)] = 1
	
	#set the restocked quantity now that we no longer need the old quantity, append the restock to the log and save.
	product.quantity = int(restockQuantity)
	
	a.append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": int(restockQuantity)})
	
	product.save()
	
	#run the machine learning code on this to make a new learned prediction now that all the needed data is in the database
	gradient(bar)

def predict(bar):
	query = []
	quantity = []
	date = []
	
	#get the products database info and copy it into a local variable
	product = productDoc.view("products/admin", key=bar).first()
	
	a = product.log
	
	#sort the log just incase it's not in order when you get it
	query = sorted(a, key=lambda a: a['date'], reverse=True)
	
	m = len(query)
	
	dateTime = datetime.datetime.strptime(query[0]['date'], '%Y-%m-%d %H:%M:%S')

	#calculate the differences in days relative to the last change in products for the peak
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
	
	#difference = date[i]
	
	#its 2am and I got bored with standard naming conventions...
	bob = thorVector(date)
	sara = thorVector(quantity)
	frank = thorVector([])
	raven = []
	
	#take the partial deriv of each part of the vector to gain the total deriv or gradient...
	for d in range(len(bob)):
		frank.append(polyderiv([sara[d],-bob[d],-math.pow(-bob[d], 2)]))
	
	#then try to make the rate from the derivative data...
	if frank[len(frank)-1][0]:
		try:
			yoyo = float(sara[1]/frank[1][0])
		except:
			yoyo = 'NED'
	else:
		yoyo = 'NED'

	#if we had enough data to calculate a rate, use it to 
	if yoyo != 'NED':
		spider = abs(float(sara[1]/yoyo))
	else:
		spider = 'NED'
	
	if spider is frank[1][0]:
		f = open("/tmp/predictTrue", "wr")
		f.write("True")
		f.close()
		
	if (str(yoyo)) in product.allPredictedRate:
		product.allPredictedRate[str(abs(yoyo))] += 1
	else:
		product.allPredictedRate[str(abs(yoyo))] = 1
	
	if (str(spider)) in product.allPredictedDay:
		product.allPredictedDay[str(spider)] += 1
	else:
		product.allPredictedDay[str(spider)] = 1
	
	product.predicted['days'] = spider
	product.predicted['rate'] = abs(yoyo)
	
	product.save()
	
	#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
	#Ie: Raptor eats everything... nom nom nom
	#raptor = {'rate': yoyo, 'days': abs(spider), 'total': (abs(difference)+abs(spider))}
	
	#return raptor

def gradient(bar):
	'''
	Note: It is assumed that the product has used data if it is being restocked, and the functions which call 
	this one make sure that all the needed data is already in the database before passing control to 
	this .
	
	This tries to (hopefully) do a simple gradient descent over time with the rate and days to make a fairly acurate 
	prediction. It uses both the correct and the predicted rates to make a weight which is applied to the current 
	correct rate and days to make a "learned" rate and days. This is then used to make a "learned" prediction 
	which will hopefully be able to get fairly close to when a product is going to run out, based off of previous 
	usage rates and patterns.
	
	This may still need a ton of work (actually I know it'll need a ton more work so please ignore this at the moment 
	until it makes it way into the commit log as official. Thanks!
	'''
	product = productDoc.view("products/admin", key=bar).first()
	
	#first pull in all the data needed from the database into local copies for ease of typing mainly
	'''
	Not currently used since I'm just using the current predictions and correct values for each rate and day
	rather than calculating an average or something.
	allPredictedRate = product.allPredictedRate
	allPredictedDay = product.allPredictedDay
	allCorrectRate = product.allCorrectRate
	allCorrectRate = product.allCorrectDay
	'''
	
	currentCorrectRate = product.correct['rate']
	currentCorrectDay = product.correct['days']
	
	currentPredictedRate = product.predicted['rate']
	currentPredictedDay = product.predicted['days']
	
	#now calculate the weight for the rate and days by squaring the difference between the
	#correct and predicted values
	rateWeight = math.pow((currentCorrectRate - currentPredictedRate), -2)
	dayWeight = math.pow((currentCorrectDay - currentPredictedDay), -2)
	
	#store the new weights into the buckets which we use to easily calculate the
	#average of the rate and day weights
	if str(rateWeight) in product.weightedRate:
		product.weightedRate[str(rateWeight)] += 1
	else:
		product.weightedRate[str(rateWeight)] = 1
	
	if str(dayWeight) in product.weightedDay:
		product.weightedDay[str(dayWeight)] += 1
	else:
		product.weightedDay[str(dayWeight)] = 1
	
	#from the buckets, calculate the average of the weights to use to make the new prediction
	#This should help it eventually get to a fairly accurate prediction
	weightedDaysAveragePre = 0
	weightedDaysAverageCount = 0
		
	for key in product.weightedDay:
		weightedDaysAveragePre += float(key) * product.weightedDay[key]
		weightedDaysAverageCount += product.weightedDay[key]
	
	weightedDaysAverage = weightedDaysAveragePre/weightedDaysAverageCount
	
	weightedRateAveragePre = 0
	weightedRateAverageCount = 0
		
	for key in product.weightedRate:
		weightedRateAveragePre += float(key) * product.weightedRate[key]
		weightedRateAverageCount += product.weightedRate[key]
	
	weightedRateAverage = weightedRateAveragePre/weightedRateAverageCount
	
	#now apply the average weights to the current correct day and rates to
	#make learned days and rates
	weightedDays = weightedDaysAverage * currentCorrectDay
	weightedRate = weightedRateAverage * currentCorrectRate
	
	#now use the learned days and rates to make a learned prediction
	learnedPrediction = weightedDays/weightedRate
	
	#store it all for  future reference
	product.learned['predicted'] = learnedPrediction
	product.learned['rate'] = weightedRate
	product.learned['days'] = weightedDays
	
	#save it and hope we did it right, if we did we don't return anything
	#(nothing to really return at this point
	product.save()