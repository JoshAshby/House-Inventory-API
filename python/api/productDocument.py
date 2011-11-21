#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
productDoc database document class

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
from dateutil.relativedelta import relativedelta

class productDoc(couchdbkit.Document):
	barcode = couchdbkit.StringProperty()
	picture = couchdbkit.StringProperty()
	name = couchdbkit.StringProperty()
	doc_type = couchdbkit.StringProperty()
	category = couchdbkit.StringProperty()
	description = couchdbkit.StringProperty()
	flag = couchdbkit.StringProperty()
	
	doc_type = "productDoc"
	
	quantity = couchdbkit.IntegerProperty()
	rank = couchdbkit.IntegerProperty
	
	tags = couchdbkit.ListProperty()
	log = couchdbkit.ListProperty()
	
	allPredictedRate = couchdbkit.DictProperty()
	allCorrectRate = couchdbkit.DictProperty()
	weightedRate = couchdbkit.DictProperty()
	allCorrectDay = couchdbkit.DictProperty()
	predicted = couchdbkit.DictProperty()
	learned = couchdbkit.DictProperty()
	correct = couchdbkit.DictProperty()
	
	def restock(self, restockQuantity):
		a = self.log
		
		#sort the log just incase it's not in order when you get it
		query = sorted(a, key=lambda a: a['date'], reverse=True)
		
		m = len(query)
		
		dateTimeNow = datetime.datetime.now()
		dateTimeLast = datetime.datetime.strptime(query[0]['date'], '%Y-%m-%d %H:%M:%S')
		
		date = []
		quantity = []
		
		#calculate the differences in days relative to the last change in products for the peak
		for i in range(m):
			if (i+1) == m:
				quantity.append(float(query[i]['quantity']))
				date.append(float((dateTimeLast - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
				break
			elif (query[i]['quantity'] > query[i+1]['quantity']):
				quantity.append(float(query[i]['quantity']))
				date.append(float((dateTimeLast - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
				break
			else:
				quantity.append(float(query[i]['quantity']))
				date.append(float((dateTimeLast - datetime.datetime.strptime(query[i]['date'], '%Y-%m-%d %H:%M:%S')).days))
		
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
		
		#add the predictions to the buckets for future reference and then also store the most
		#recent in a seperate variable in the database
		if (str(abs(yoyo))) in self.allPredictedRate:
			self.allPredictedRate[str(abs(yoyo))] += 1
		else:
			self.allPredictedRate[str(abs(yoyo))] = 1
		
		self.predicted['rate'] = abs(yoyo)
		
		#calculate the difference between now and the last time the quantity changed, ie: the time
		#it took for the product to reach zero. Then store the correct values in the database
		correctDay = float((dateTimeNow - dateTimeLast).days)
		
		if str(correctDay) in self.allCorrectDay:
			self.allCorrectDay[str(correctDay)] += 1
		else:
			self.allCorrectDay[str(correctDay)] = 1
		
		#calculate the correctRate by taking the current quantity and dividing it by the number of days it took to reach zero
		#then store it in the bucket list for furture needs
		correctRate = float(self.quantity/correctDay)
		
		#store the current correct values for easy access in gradient()
		self.correct['rate'] = correctRate
		
		if str(correctRate) in self.allCorrectRate:
			self.allCorrectRate[str(correctRate)] += 1
		else:
			self.allCorrectRate[str(correctRate)] = 1
		
		self.quantity = restockQuantity
	
		a.append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": restockQuantity})
	
		#first pull in all the data needed from the database into local copies for ease of typing mainly
		currentCorrectRate = self.correct['rate']
		
		currentPredictedRate = self.predicted['rate']
		
		#now calculate the weight for the rate and days by squaring the difference between the
		#correct and predicted values
		rateWeight = math.pow((currentCorrectRate - currentPredictedRate), -2)

		weightedRate = rateWeight * currentCorrectRate
		
		#store the new weights into the buckets which we use to easily calculate the
		#average of the rate and day weights
		if str(weightedRate) in self.weightedRate:
			self.weightedRate[str(weightedRate)] += 1
		else:
			self.weightedRate[str(weightedRate)] = 1
		
		#from the buckets, calculate the average of the weights to use to make the new prediction
		#This should help it eventually get to a fairly accurate prediction
		weightedRateAveragePre = 0
		weightedRateAverageCount = 0
			
		for key in self.weightedRate:
			weightedRateAveragePre += float(key) * self.weightedRate[key]
			weightedRateAverageCount += self.weightedRate[key]
		
		weightedRateAverage = weightedRateAveragePre/weightedRateAverageCount
		
		#now use the learned days and rates to make a learned prediction
		learnedPrediction = (self.quantity)/weightedRateAverage
		
		#store it all for  future reference
		self.learned['predicted'] = learnedPrediction
		self.learned['rate'] = weightedRate
		
		self.save()
		
		daysFromNow = datetime.datetime.strftime(datetime.datetime.now() + relativedelta(days=learnedPrediction), '%Y-%m-%d %H:%M:%S')
		
		return [learnedPrediction, daysFromNow]
		
		
	def order(self, quantity):
		self.quantity = quantity
		self.log.append({"date": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"), "quantity": quantity})
		self.save()


productDoc.set_db(database)