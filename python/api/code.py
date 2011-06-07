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
#Don't ask... this error is just better than a standard raise
class MathError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
class thorVector(object):
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
	def GET(self):
		return render.index()

class info:
	def GET(self, barcode):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class total:
	def GET(self):
		query = []
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i])
		web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class add:
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
	def GET(self, barcode):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		db.query('DELETE FROM products WHERE barcode = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class names:
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
		
		bob = thorVector(date)
		sara = thorVector(quantity)
		
		
		frank = thorVector([])
		dr = thorVector([])
		
		
		for n in range(len(bob)):
			frank.append(0)
			dr.append(0)
			
		#testing section: 
		if debug:
			return json.dumps([len(bob),len(frank)])
		'''
		This is waht we need to solve for: it should give us the x intercept as being the number of days on average if the pattern was to continue at the given rate
		bob = sara+dr*sara^2+frank
		'''
		
		#not being used just yet since we need to solve the system first
		#web.header('Content-Type', 'application/json')
		#return json.dumps(log)
		
if __name__ == "__main__":
	app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()