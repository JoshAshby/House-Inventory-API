#!/usr/bin/env python
import web
import json
import re
import time
"""
Basic math type implimentation for Python. Very basic, nothing fancy.

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""

'''
For some reason, python and web.py don't want to import this file so for the time being it's in here (get an error if you try to import it...)
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111] mod_wsgi (pid=2395): Target WSGI script '/srv/http/code.py' cannot be loaded as Python module.
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111] mod_wsgi (pid=2395): Exception occurred processing WSGI script '/srv/http/code.py'.
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111] Traceback (most recent call last):
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111]   File "/srv/http/code.py", line 6, in <module>
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111]     from linear import *
[Tue Jun 07 00:50:01 2011] [error] [client 192.168.1.111] ImportError: No module named linear
'''

#debug setter
spamandeggs = 0

#Don't ask... this error is just better than a standard raise
class MathError(Exception):
	'''
	class documentation
	MathError for use by the Vector
	'''
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
class thorVector(object):
	'''
	class documentation
	Creates a Vector type for Python. More coming soon.
	'''
	#Even though it's not that powerful...
	def __init__(self, data=[]):
		self.data = data
	
	def __repr__(self):
		return repr(self.data)
		
	def __getitem__(self, index):
		return self.data[index]

	def __len__(self):
		return len(self.data)
	
	def __add__(self, other):
		data = []
		if type(other) == self.__class__:
			for j in range(len(self.data)):
				data.append(self.data[j] + other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')
		
	def __sub__(self, other):
		data = []
		if len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] - other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')

	def __mul__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] * other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			result = None
			for j in range(len(self.data)):
				data.append(self.data[j] * other.data[j])
			for i in range(len(self.data)-1):
				result = data[i] + data [i-1]
			return self.__class__(result)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
	
	def __div__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] / other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] / other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
		
	def __pow__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] ** other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] ** other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
			
	def __radd__(self, other):
		data = []
		if type(other) == self.__class__:
			for j in range(len(self.data)):
				data.append(self.data[j] + other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')
		
	def __rsub__(self, other):
		data = []
		if len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] - other.data[j])
			return self.__class__(data)
		else:
			raise MathError('What the hell? It *must* (MUST) be another Vector object! NOTHING ELSE!')

	def __rmul__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] * other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			result = None
			for j in range(len(self.data)):
				data.append(self.data[j] * other.data[j])
			for i in range(len(self.data)-1):
				result = data[i] + data [i-1]
			return self.__class__(result)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
	
	def __rdiv__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] / other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] / other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
		
	def __rpow__(self, other):
		data = []
		if type(other) == int:
			for j in range(len(self.data)):
				data.append(self.data[j] ** other)
			return self.__class__(data)
		elif len(self.data) == len(other):
			for j in range(len(self.data)):
				data.append(self.data[j] ** other.data[j])
			return self.__class__(data)
		else:
			raise MathError('Really? It *must* be a Vector of the same length or a plain old integer! Gosh, get it right...')
	
	def insert(self, where, what):
		self.data.insert(where, what)
	
	def append(self, what):
		self.data.append(what)
		
	def pop(self, where):
		return self.data.pop(where)
		
	def average(self):
		avg_undiv = 0
		for w in range(len(self.data)):
			avg_undiv =+ self.data[w]
		avg = avg_undiv/(len(self.data)+1)
		return avg
		
#Start main web.py app:

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='barcode')
        
urls = (
	'/', 'index',
	'/product/(.*)/info/', 'info',
	'/product/(.*)/delete/', 'delete',
	'/product/(.*)/(.*)/(.*)/(.*)/add/', 'add',
	'/product/(.*)/(.*)/(.*)/(.*)/update/', 'update',
	'/product/(.*)/(.*)/order/', 'order',
	'/product/', 'total',
	'/product/names/', 'names',
	'/product/(.*)/log/', 'log',
	'/product/(.*)/stats/', 'stats'
)

render = web.template.render('/srv/http/template/')

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
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class total:
	'''
	class documentation
	Returns all the product info. Used for product info tables in the main client
	'''
	def GET(self):
		query = []
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i])
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
		db.query('INSERT INTO products (name, description, barcode, quantity) VALUES ($name, $description, $barcode, $quantity)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['added'] = 'true'
		db.query('INSERT INTO stats (barcode, quantity) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
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
		db.query('UPDATE products SET name = $name, description = $description, barcode = $barcode, quantity = $quantity WHERE barcode = $barcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['updated'] = 'true'
		db.query('INSERT INTO stats (barcode, quantity) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class order:
	'''
	class documentation
	More coming soon, since this is pretty worthless right now...
	'''
	def GET(self, barcode, quantity):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		quant = inform['quantity']
		quantity = quant - quantity
		db.query('UPDATE products SET quantity = $quantity WHERE barcode = $barcode', vars={'quantity': quantity , 'barcode': barcode})
		inform['ordered'] = 'true'
		db.query('INSERT INTO stats (barcode, quantity) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class delete:
	'''
	class documentation
	Deletes the given product.
	'''
	def GET(self, barcode):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		db.query('DELETE FROM products WHERE barcode = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class names:
	'''
	class documentation
	Generates a list of names and barcodes for auto complete
	'''
	def GET(self):
		query = []
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i]['name'])
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i]['barcode'])
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
		name = db.query('SELECT quantity, date FROM stats WHERE barcode = $barcode', vars={'barcode':barcode})
		for i in range(len(name)):
			query.append(name[i])
		for i in range(len(query)):
			log.append([query[i]['date'].isoformat(' '), query[i]['quantity']])
		web.header('Content-Type', 'application/json')
		return json.dumps(log)


class stats:
	'''
	class documentation
	Generates stats about the given product.
	'''
	def GET(self, barcode):
		query = []
		quantity = []
		date = []
		
		name = db.query('SELECT quantity, date FROM stats WHERE barcode = $barcode ORDER BY date desc', vars={'barcode':barcode})
		
		for i in range(len(name)):
			query.append(name[i])
		
		m = len(query)
		
		for i in range(m):
			if (query[i]['quantity'] < query[i+1]['quantity']):
				quantity.append(int(query[i]['quantity']))
				date.append((query[0]['date'] - query[i]['date']).days)
			else:
				quantity.append(int(query[i]['quantity']))
				date.append((query[0]['date'] - query[i]['date']).days)
				break
		
		#its 2am and I got bored with standard naming conventions...
		bob = thorVector(date)
		sara = thorVector(quantity)
		frank = thorVector([])
		
		for n in range(len(bob)):
			frank.append(0)
			
		#testing section: 
		if spamandeggs:
			return json.dumps([len(bob),len(frank)])
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
		'''
		
		#interesting combo... typically to make a new person, wouldn't one add the people? or multiply?
		frank = sara - bob - bob**2
		#Derivative should be taken
		
		'''
		#at this point I need to take the derivative to get the slope at each point, at which time I'll be able to make the equation for the line which these points form
		#the intercept of this line is how many days the current stock will run out at. This will then be converted into a standard dataset, by dividing the quantity by this guess.
		#The machine learning bit will be using this standardized approximation and storie it each time in two columns of the product database. 
		#This first will be a rolling list of the last five guesses, the second will be a list of every one made for reference purposes.
		#The reason for standardizing them is because the units then become how many days per one unit, which makes it easy to just take the average of the last
		#5 guesses to try and make a better guess. It'll also learn from everytime the stock reaches zero.
		'''
		
		#just something to return until this bit of code is finished.
		#Yes, frank is also a raptor if called properly...
		raptor = frank.average()
		
		#web.header('Content-Type', 'application/json')
		return json.dumps(str(raptor))
		
if __name__ == "__main__":
	app.run()

#wsgi stuff
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()