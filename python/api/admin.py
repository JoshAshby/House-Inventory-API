#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API that provides public and admin functions.
Admin calls to the API must be POST and use OAUTH1 2-legged.
This is the main app, which calls upon other sub apps according to whats needed.
This also holds useless test and index classes.

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
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from ashmath import *
from configSub import *
from ashpic import *
import auth
import account

urls = (
	'', 'slash',
	'/(.*)/delete/', 'delete',
	'/(.*)/restore/', 'restore',
	'/(.*)/log/', 'log',
	'/(.*)/stats/', 'stats',
	'/add/', 'add',
	'/update/', 'update'
)

class slash:
	def GET(self): raise web.seeother("/")

GET_UNAUTHORIZED_MESSAGE = "Your not able to access this from GET and need OAuth to be able to access any of the POST resources for Admins"

class add:
	'''
	class documentation
	Adds the given product from the POST data.
	
	Returns:
		A JSON object like: {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53}
	'''
	
	def GET(self):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self):
		bobbins= web.input(picture={})
		
		#if there is data in the Post go through the stuff to add it to the table if not, then let the client know there was no data sent...
		if bobbins['barcode'] and bobbins['name'] and bobbins['description'] and bobbins['quantity']:
			name = bobbins['name']
			barcode = bobbins['barcode']
			description = bobbins['description']
			quantity = bobbins['quantity']
			if 'cat' in bobbins: quantity = bobbins['cat']
			else: cat = 'None'
			pictureTrue = int(bobbins['picTrue'])
			picture = bobbins.picture
			
			query = []
			copy = 0
			
			names = db.query('SELECT `barcode` FROM `products`')
			for i in range(len(names)):
				query.append(names[i])
			
			for k in range(len(query)):
				if (query[k]['barcode'] == barcode):
					return json.dumps({'COP': barcode})
				else:
					pass

			if pictureTrue == 1:
				catdog = re.search('(\..*)', picture.filename).group()
				
				frodo = barcode + catdog
				
				f = open(abspath + '/pictures/' + frodo, "wb")

				while 1:
					chunk = picture.file.read(10000)
					if not chunk:
						break
					f.write( chunk )
				f.close()
				
				goop = freyaPics(frodo)
				goop.odinsThumb()
			else:
				frodo = 'NULL'
			
			p = re.compile('\+')
			found = p.sub( ' ', description)
			db.query('INSERT INTO `products` (`name`, `description`, `barcode`, `quantity`, `picture`, `cat`) VALUES ($name, $description, $barcode, $quantity, $picture)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode, 'picture':frodo, 'cat': cat})
			name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
			inform = name[0]
			inform['added'] = 'true'
			db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
			db.query('INSERT INTO `stats` (`barcode`, `last_5`, `all`) VALUES ($barcode, "[]", "[]")', vars={'barcode': barcode})
			if spam:
				web.header('Content-Type', 'application/json')
			return json.dumps(inform)
		else:
			return json.dumps(['NS'])


class update:
	'''
	class documentation
	Updates the given product from the POST data.
	
	Returns:
		A JSON object like: {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53}
	
		Where:
			oldbarcode = the previous barcode incase the barcode was changed.
	'''
	
	def GET(self):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self):
		bobbins= web.input(picture={})
		
		if bobbins['barcode']:
			the_ring = []
			
			barcode = bobbins['barcode']
			
			bilbo = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
			
			for e in range(len(bilbo)):
				the_ring.append(bilbo[e])
			
			if 'name' in bobbins: name = bobbins['name']
			else: name = the_ring[0]['name']
			
			if 'newbarcode' in bobbins: oldbarcode = bobbins['newbarcode']
			else: oldbarcode = the_ring[0]['barcode']
			
			if 'description' in bobbins: description = bobbins['description']
			else: description = the_ring[0]['description']
			
			if 'quantity' in bobbins: quantity = bobbins['quantity']
			else: quantity = the_ring[0]['quantity']
			
			if 'cat' in bobbins: cat = bobbins['cat']
			else: cat = the_ring[0]['cat']
			
			if 'picTrue' in bobbins: pictureTrue = int(bobbins['picTrue'])
			picture = bobbins.picture
			
			if pictureTrue == 1:
				catdog = re.search('(\..*)', picture.filename).group()
				
				frodo = barcode + catdog
				
				f = open(abspath + '/pictures/' + frodo, "wb")

				while 1:
					chunk = picture.file.read(10000)
					if not chunk:
						break
					f.write( chunk )
				f.close()
				
				goop = freyaPics(frodo)
				goop.odinsThumb()
				
			else:
				frodo = the_ring[0]['picture']
			
			p = re.compile('\+')
			found = p.sub( ' ', description)
			
			db.query('UPDATE `products` SET `name` = $name, `description` = $description, `barcode` = $barcode, `quantity` = $quantity, `picture` = $picture, `cat` = $cat WHERE `barcode` = $oldbarcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': oldbarcode, 'picture': frodo, 'oldbarcode': barcode, 'cat': cat})
			
			if oldbarcode is not barcode:
				db.query('UPDATE `stats` SET `barcode` = $barcode WHERE `barcode` = $oldbarcode', vars={'barcode': oldbarcode, 'oldbarcode': barcode})
				db.query('UPDATE `usage` SET `barcode` = $barcode WHERE `barcode` = $oldbarcode', vars={'barcode': oldbarcode, 'oldbarcode': barcode})
				
			db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': oldbarcode})
			name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode': oldbarcode})
			
			inform = name[0]
			inform['updated'] = 'true'
			inform['oldbarcode'] = barcode
			inform['barcode'] = oldbarcode
			if spam:
				web.header('Content-Type', 'application/json')
			return json.dumps(inform)
		else:
			return json.dumps(['NS'])


class delete:
	'''
	class documentation
	Deletes the given product. And moves it's information into the backup table for reference later or restoration.
	
	Returns:
		A JSON object like: {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52, "thumb": "dog_thumb.png"}
	'''
	
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, barcode):
		log = []
		vallog = []
		
		name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		inform = name[0]
		
		stated = db.query('SELECT * FROM `stats` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		stat = stated[0]
			
		loged = db.query('SELECT `date`, `quantity` FROM `usage` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		for x in range(len(loged)):
			vallog.append(loged[x])
			val = {'date': vallog[x]['date'].isoformat(' '), 'quantity': vallog[x]['quantity']}
			log.append(val)
		
		logSON = json.dumps(log)
		
		db.query('INSERT INTO `backup` (`id`, `barcode`, `name`, `description`, `quantity`, `cat`, `picture`, `flag`, `last_5`, `all`, `log`) VALUES ($id, $barcode, $name, $description, $quantity, $cat, $picture, $flag, $last_5, $all, $log) ', vars={'barcode': inform['barcode'], 'name': inform['name'], 'quantity':inform['quantity'], 'id': inform['id'], 'description': inform['description'], 'quantity': inform['quantity'], 'cat': inform['cat'], 'picture': inform['picture'], 'flag': inform['flag'], 'last_5': stat['last_5'], 'all': stat['all'], 'log': logSON})
		
		db.query('DELETE FROM `products` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		db.query('DELETE FROM `stats` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		db.query('DELETE FROM `usage` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)


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
		
		db.query('INSERT INTO `products` (`id`, `barcode`, `name`, `description`, `quantity`, `cat`, `picture`, `flag`) VALUES ($id, $barcode, $name, $description, $quantity, $cat, $picture, $flag) ', vars={'barcode': inform['barcode'], 'name': inform['name'], 'quantity':inform['quantity'], 'id': inform['id'], 'description': inform['description'], 'cat': inform['cat'], 'picture': inform['picture'], 'flag': inform['flag']})
		
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
		A JSON object like: {"names" : [["2011-03-19 01:15:17", 1], ["2011-02-19 01:15:09", 2], ["2011-02-06 00:47:43", 6], ["2011-02-05 00:47:43", 3]]}
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
		#A JSON object like: {"current": -28.0, "guess": -0.07142857142857142, "predictedNF": -28, "predicted": -28.0, "standard": -0.07142857142857142}
		
		Where:
			current = current rate at which the product will run out based off of the current log
			guess: = standard form rate of the predicted time
			predictedNF = int form of the predicted value
			predicted = the predicted rate for when the product will run out, as guessed by the last_5 guesses
			standard = standard form of current
			rank = the over all numerical rank of the product.
			popularity = High, Med, Low, or NED
	'''
	
	def GET(self, barcode):
		raise web.unauthorized(GET_UNAUTHORIZED_MESSAGE)
		
	@auth.oauth_protect
	def POST(self, barcode):
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
		at this point I need to take the derivative to get the slope at each point, at which time I'll be able to make the equation for the line which these points form
		the intercept of this line is how many days the current stock will run out at. This will then be converted into a standard dataset, by dividing the quantity by this guess.
		The machine learning bit will be using this standardized approximation and storie it each time in two columns of the product database. 
		This first will be a rolling list of the last five guesses, the second will be a list of every one made for reference purposes.
		The reason for standardizing them is because the units then become how many days per one unit, which makes it easy to just take the average of the last
		5 guesses to try and make a better guess. It'll also learn from everytime the stock reaches zero.
		
		These next few lines are all very messy, however they work well. The goal is to simply make a few calculations to get the standard rate and the guessed rate, and store everything into the table, 
		if there is not enough data then simply state that, and continue on with nothing.
		It makes it nice because the rolling list goes across peaks, and without errors the come up. if there is a 0 rate, it simply gets ignored (I think... hopefully)
		'''
		
		#take the partial deriv of each part of the vector to gain the total deriv or gradient...
		for d in range(len(bob)):
			frank.append(polyderiv([sara[d],-bob[d],-bob[d]**2]))
		
		#if there is a rate to convert
		if frank[len(frank)-1][0]:
			#make the standard rate...
			yoyo = sara[1]/frank[1][0]
		else:
			yoyo = 'NED'
			
		'''
		These next few lines go through and do the rolling list and total rates for the product
		rates are the intercepts of the gradient.
		These rates are stored in the database table 'stats' and are stored as json objects for ease of use and storage.
		
		Warning: they are messy, and everything is wrapped in a try: except block because most of this needs data, which
		sometimes isn't there so you have to come up with other ways of working with the data, or return NED, or Not Enough Data.
		'''
		
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
		
		if yoyo != 'NED':
			last_5.append(yoyo)
			all.append(yoyo)
		
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
			if batman != 'NED':
				spider = sara[1]/batman
				intSpider = int(spider)
			else:
				spider = 'NED'
				intSpider = 'NED'
		except:
			spider = 'NED'
			intSpider = 'NED'
		
		#and now I have the hic-ups...
		db.query('UPDATE `stats` SET `last_5` = $last_5, `all` = $all WHERE `barcode` = $barcode', vars={'last_5': json.dumps(last_5), 'all': json.dumps(all) , 'barcode': barcode})
		
		try:
			if frank[1][0]:
				current = frank[1][0]
			else:
				current = 'NED'
		except:
			current = 'NED'
			
		'''
		Next bit here calculates the popularity compared to other products, based off of the last predicted standard...
		
		What we need to do, is look at all the standard rates, and see which are the lowest, and make a comparison between
		all the rates. IE: product x is ranked lower than product y, and place all the products into an array (this may later need to be cut up by
		product type (which is coming soon sometime) to help ease processing time and power needed).
		'''
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
		#raptor = {'current': current, 'standard':  yoyo, 'guess': batman, 'predicted': spider, 'predictedNF': intSpider}
		raptor = {'predicted': spider, 'rank': soda, 'popularity': ger}
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(raptor)


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()