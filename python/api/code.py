#!/usr/bin/env python
import web
import json
import re
import time

'''
From: http://webpy.org/install
and 
http://code.google.com/p/modwsgi/wiki/ApplicationIssues

This must be done to avoid the import errors which come up with having linear.py and config.py
'''
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from ashmath import *
from config import *


"""
Project Blue Ring
A scalable inventory control and management system based in the cloud.

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""

class index:        
	'''
	class documentation
	Base Index...
	'''
	def GET(self):
		return render.index()

class info:
	'''
	class documentation
	Info about the given product.
	'''
	def GET(self, barcode):
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class total:
	'''
	class documentation
	Returns all the product info. Used for product info tables in the main client
	'''
	def GET(self):
		query = []
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class add:
	'''
	class documentation
	Adds the given product.
	'''
	def GET(self, barcode, name, quantity, description):
		p = re.compile('\+')
		found = p.sub( ' ', description)
		db.query('INSERT INTO `products` (`name`, `description`, `barcode`, `quantity`) VALUES ($name, $description, $barcode, $quantity)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['added'] = 'true'
		db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		db.query('INSERT INTO `stats` (`barcode`) VALUES ($barcode)', vars={'barcode': barcode})
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class update:
	'''
	class documentation
	Updates the given product.
	'''
	def GET(self, barcode, name, quantity, description):
		p = re.compile('\+')
		found = p.sub( ' ', description)
		db.query('UPDATE `products` SET `name` = $name, `description` = $description, `barcode` = $barcode, `quantity` = $quantity WHERE `barcode` = $barcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['updated'] = 'true'
		db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class order:
	'''
	class documentation
	More coming soon, since this is pretty worthless right now...
	'''
	def GET(self, barcode, quantity):
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		quant = inform['quantity']
		quantity = quant - quantity
		db.query('UPDATE `products` SET `quantity` = $quantity WHERE `barcode` = $barcode', vars={'quantity': quantity , 'barcode': barcode})
		inform['ordered'] = 'true'
		db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class delete:
	'''
	class documentation
	Deletes the given product.
	'''
	def GET(self, barcode):
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		db.query('DELETE FROM `products` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class names:
	'''
	class documentation
	Generates a list of names and barcodes for auto complete
	'''
	def GET(self):
		query = []
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i]['name'])
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i]['barcode'])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class log:
	'''
	class documentation
	Generates the use log about the given product.
	'''
	def GET(self, barcode):
		query = []
		log = []
		name = db.query('SELECT `quantity`, `date` FROM `usage` WHERE `barcode` = $barcode ORDER BY `date` desc', vars={'barcode':barcode})
		for i in range(len(name)):
			query.append(name[i])
		for i in range(len(query)):
			log.append([query[i]['date'].isoformat(' '), query[i]['quantity']])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(log)


class stats:
	'''
	class documentation
	Generates stats about the given product.
	Currently this just replies with the intercept of the slope of the line formed by the datapoints from the stats table. This is the predicted time when the current amount of food will run out.
	'''
	def GET(self, barcode):
		query = []
		quantity = []
		date = []
		
		name = db.query('SELECT `quantity`, `date` FROM `usage` WHERE `barcode` = $barcode ORDER BY `date` desc', vars={'barcode':barcode})
		
		for i in range(len(name)):
			query.append(name[i])
		
		m = len(query)
		
		for i in range(m):
			if (query[i]['quantity'] < query[i+1]['quantity']):
				quantity.append(float(query[i]['quantity']))
				date.append(float((query[0]['date'] - query[i]['date']).days))
			else:
				quantity.append(float(query[i]['quantity']))
				date.append(float((query[0]['date'] - query[i]['date']).days))
				break
		
		#its 2am and I got bored with standard naming conventions...
		'''
		Plus the fact that my vectors arn't needed currently because of the way the math has worked out,
		but its cooler to say it's running your own math type, and plus you never know, in the future there
		might be a need for a vector...
		'''
		bob = thorVector(date)
		sara = thorVector(quantity)
		frank = thorVector([])
		raven = []

		'''
		This is what we need to solve for: it should give us the x intercept as being the number of days on average if the pattern was to continue at the given rate
		sara = bob+bob^2
		in R we do something like this: (in rpy2 format)
		r['lm']('quantity_y ~cbind(date_x,(date_x)^2)')
		which runs a linear regression on the dataset which now looks something like this (for one line of the vectors)
		5 = 2+2**2+x
		which is really just 5-2-2**2 = x and then the derivative of that...
		so we just set that up in python also
		Because it's all in Vector form already, it works just as if this was linear math (funny that...) so everything is solved for properly
		#at this point I need to take the derivative to get the slope at each point, at which time I'll be able to make the equation for the line which these points form
		#the intercept of this line is how many days the current stock will run out at. This will then be converted into a standard dataset, by dividing the quantity by this guess.
		#The machine learning bit will be using this standardized approximation and storie it each time in two columns of the product database. 
		#This first will be a rolling list of the last five guesses, the second will be a list of every one made for reference purposes.
		#The reason for standardizing them is because the units then become how many days per one unit, which makes it easy to just take the average of the last
		#5 guesses to try and make a better guess. It'll also learn from everytime the stock reaches zero.
		
		These next few lines are all very messy, however they work well. The goal is to simply make a few calculations to get the standard rate and the guessed rate, and store everything into the table, 
		if there is not enough data thennnnn simply state that, and continue on with nothing.
		It makes it nice because the rolling list goes across peaks, and without errors the come up. if there is a 0 rate, it simply gets ignoerd (I think... hopefully)
		'''
		
		#take the partial deriv of each part of the vector to gain the total deriv or gradient...
		for d in range(len(bob)):
			frank.append(polyderiv([sara[d],-bob[d],-bob[d]**2]))
		
		#if there is a rate to convert
		if frank[len(frank)-1][0]:
			#make the standard rate...
			yoyo = sara[len(sara)-1]/frank[len(frank)-1][0]
		else:
			yoyo = 'Not Enough Data'
			
		'''
		These next few lines go through and do the rolling list and total rates for the product
		rates are the intercepts of the gradient.
		These rates are stored in the database table 'stats' and are stored as json objects for ease of use and storage.
		'''
		
		#load the stats info
		stat  = db.query('SELECT `last_5`, `all` FROM `stats` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		
		#error prevention stuff...
		for q in range(len(stat)):
			raven.append(stat[q])
		
		#load everything from the query into the proper variables...
		try:
			last_5Raw = raven[0]['last_5']
		except:
			lasat_5Raw = []
			
		try:
			allRaw = raven[0]['all']
		except:
			allRaw = []
		
		#try to load the json, if that fails, it means that there is no data for this product yet, so generate a list
		try:
			last_5 = json.loads(last_5Raw)
		except:
			last_5 = []
		
		#try to load the json, if that fails, it means that there is no data for this product yet, so generate a list
		try:
			all = json.loads(allRaw)
		except:
			all = []
		
		#try to do a rolling list thingy...
		try:
			if len(last_5) == 5:
				last_5.pop(0)
			else:
				pass
		except:
			pass
		
		#if you do have stuff to put into it...
		#if you don't have anything to put into it, then don't put 'not enough data' into the table...
		if yoyo != 'Not Enough Data':
			#add the rates to the list...
			last_5.append(yoyo)
			all.append(yoyo)
		
		#if there is a rate...
		if frank[len(frank)-1][0]:
			try:
				#take the average to try and make a better guess...
				batman = reduce((lambda x, y: x + y), last_5)/5
			except:
				pass
		else:
			batman = 'Not Enough Data'
			#He's a ninja...
		
		#and now I have the hic-ups...
		db.query('UPDATE `stats` SET `last_5` = $last_5, `all` = $all WHERE `barcode` = $barcode', vars={'last_5': json.dumps(last_5), 'all': json.dumps(all) , 'barcode': barcode})
			
		#Yes, frank is also a raptor if called properly...
		#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
		#Ie: Raptor eats everything... nom nom nom
		raptor = {'rate': frank[len(frank)-1][0], 'standard rate':  yoyo, 'guessed rate': batman}
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(raptor)
		
if __name__ == "__main__":
	app.run()

#wsgi stuff
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()