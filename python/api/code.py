#!/usr/bin/env python
"""
Project Blue Ring
A scalable inventory control and management system based in the cloud.

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
from config import *
from ashpic import *

class index:        
	'''
	class documentation
	Base Index...
	
	The page that is displayed if the root of the server is accessed, Currently just displays the template index.html
	'''
	def GET(self):
		return render.index()

class info:
	'''
	class documentation
	Info about the given product.
	
	returns: {"picture": "dog.png", "description": "a dog of god", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 10, "id": 52, "thumb": "dog_thumb.png"}
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
	
	returns: [{"picture": "718103025027.png", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "barcode": "718103025027", "name": "Green Graph Composition", "flag": "M", "quantity": 1, "id": 3, "thumb": "718103025027_thumb.png"}, {"picture": "3037921120217.png", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "barcode": "3037921120217", "name": "Orange Graph Notebook", "flag": "L", "quantity": 1, "id": 4, "thumb": "3037921120217_thumb.png"}]
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
	Adds the given product from the POST data.
	
	returns: {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53, "thumb": "dog_thumb.png"}
	'''
	def POST(self):
		bobbins= web.input(picture={})
		
		#if there is data in the Post go through the stuff to add it to the table if not, then let the client know there was no data sent...
		if bobbins['barcode'] and bobbins['name'] and bobbins['description'] and bobbins['quantity']:
			name = bobbins['name']
			barcode = bobbins['barcode']
			description = bobbins['description']
			quantity = bobbins['quantity']
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

			if picture is not {}:
				cat = re.search('(\..*)', picture.filename).group()
				
				frodo = barcode + cat
				pinky = barcode+ '_thumb' + cat
				
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
				pinky = 'NULL'
			
			p = re.compile('\+')
			found = p.sub( ' ', description)
			db.query('INSERT INTO `products` (`name`, `description`, `barcode`, `quantity`, `picture`, `thumb`) VALUES ($name, $description, $barcode, $quantity, $picture, $pinky)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode, 'picture':frodo, 'pinky':pinky})
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
	
	returns: {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53, "thumb": "dog_thumb.png"}
	
	Where:
		oldbarcode = the previous barcode incase the barcode was changed
	'''
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
			
			picture = bobbins.picture
			
			if picture is not {}:
				cat = re.search('(\..*)', picture.filename).group()
				
				frodo = barcode + cat
				pinky = barcode+ '_thumb' + cat
				
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
				pinky = the_ring[0]['thumb']
			
			p = re.compile('\+')
			found = p.sub( ' ', description)
			
			db.query('UPDATE `products` SET `name` = $name, `description` = $description, `barcode` = $barcode, `quantity` = $quantity, `picture` = $picture, `thumb` = $pinky WHERE `barcode` = $oldbarcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': oldbarcode, 'picture': frodo, 'oldbarcode': barcode, 'pinky': pinky})
			
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
	Deletes the given product.
	
	returns: {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52, "thumb": "dog_thumb.png"}
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
	
	returns: [{"barcode": "718103025027", "name": "Green Graph Composition"}, {"barcode": "3037921120217", "name": "Orange Graph Notebook"}, {"barcode": "043396366268", "name": "the social network"}, {"barcode": "dog987", "name": "Beagle"}]
	'''
	def GET(self):
		query = []
		names = db.query('SELECT `name`, `barcode` FROM `products`')
		for i in range(len(names)):
			query.append(names[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class log:
	'''
	class documentation
	Generates the use log about the given product.
	
	returns: [["2011-03-19 01:15:17", 1], ["2011-02-19 01:15:09", 2], ["2011-02-06 00:47:43", 6], ["2011-02-05 00:47:43", 3]]
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
	
	returns a JSON string like: {"current": -28.0, "guess": -0.07142857142857142, "predictedNF": -28, "predicted": -28.0, "standard": -0.07142857142857142}
	
	Where:
		current = current rate at which the product will run out based off of the current log
		guess: = standard form rate of the predicted time
		predictedNF = int form of the predicted value
		predicted = the predicted rate for when the product will run out, as guessed by the last_5 guesses
		standard = standard form of current
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
		if yoyo != 'NED':
			#add the rates to the list...
			last_5.append(yoyo)
			all.append(yoyo)
		
		#if there is a rate...
		try:
			if frank[1][0]:
				try:
					#take the average to try and make a better guess...
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
		
		#Yes, frank is also a raptor if called properly...
		#raptor stores everything that gets dumped to the browser as JSON so this goes after everything above....
		#Ie: Raptor eats everything... nom nom nom
		raptor = {'current': current, 'standard':  yoyo, 'guess': batman, 'predicted': spider, 'predictedNF': intSpider}
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(raptor)
		
if __name__ == "__main__":
	app.run()

#wsgi stuff
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()