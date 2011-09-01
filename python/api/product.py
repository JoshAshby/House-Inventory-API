#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main public product calls
Does not involve anything with categories, all that is in cat.py

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
try:
	from configSub import *
except:
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
from configSub import *
from ashmath import *
from ashpic import *
import auth
import account

urls = (
	'', 'slash',
	'/(.*)/', 'info',
	'/', 'total'
)

#class slash:
#	def GET(self): raise web.seeother("/")

class info:
	'''
	class documentation
	
	Product manipulation class. Functions to return the info, update and delete products are contained below, including a testing function for unittests.
	'''
	
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"picture": "dog.png", "description": "a dog of god", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 10, "id": 52}
		'''
		#Go through and make sure we're not in testing mode, in which case the unit tests will pass the barcode instead...
		try: 
			wi = web.input()
			barcode = wi['barcode']
		except:
			barcode = kwargs['barcode']
		
		#name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		name = db.select('products', where="barcode=$barcode", vars = {'barcode': barcode}, limit=1, _test=False)
		inform = name[0]
		
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
	
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
		'''
		pass
		#return self.getFunc(args)
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
			A JSON object like: {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53}
	
		Where:
			oldbarcode = the previous barcode incase the barcode was changed.
		'''
		try:
			bobbins= web.input(picture={})
		except:
			bobbins = kwargs
			if 'picture' in bobbins: pass
			else: bobbins['picture'] = {}
		
		if bobbins['barcode']:
			the_ring = []
			
			bar = bobbins['barcode']
			
			#bilbo = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
			bilbo = db.select('products', where='barcode=$barcode', vars={'barcode':bar}, limit=1, _test=False)
			
			for e in range(len(bilbo)):
				the_ring.append(bilbo[e])
			
			if 'name' in bobbins: nam = bobbins['name']
			else: nam = the_ring[0]['name']
			
			if 'newbarcode' in bobbins: oldbarcode = bobbins['newbarcode']
			else: oldbarcode = the_ring[0]['barcode']
			
			if 'description' in bobbins: desc = bobbins['description']
			else: desc = the_ring[0]['description']
			
			if 'quantity' in bobbins: quant = bobbins['quantity']
			else: quant = the_ring[0]['quantity']
			
			if 'cat' in bobbins: ca = bobbins['cat']
			else: ca = the_ring[0]['cat']
			
			if 'tags' in bobbins: tag = bobbins['tags']
			else: tag = '["None"]'
			
			if 'picTrue' in bobbins: pictureTrue = int(bobbins['picTrue'])
			else: pictureTrue = 0
			#pic = bobbins.picture
			pic = bobbins['picture']
			
			if pictureTrue == 1:
				catdog = re.search('(\..*)', pic.filename).group()
				
				frodo = bar + catdog
				
				f = open(abspath + '/pictures/' + frodo, "wb")

				while 1:
					chunk = pic.file.read(10000)
					if not chunk:
						break
					f.write( chunk )
				f.close()
				
				goop = freyaPics(frodo)
				goop.odinsThumb()
				
			else:
				frodo = the_ring[0]['picture']
			
			p = re.compile('\+')
			found = p.sub( ' ', desc)
			
			#db.query('UPDATE `products` SET `name` = $name, `description` = $description, `barcode` = $barcode, `quantity` = $quantity, `picture` = $picture, `cat` = $cat, `tags` = $tags WHERE `barcode` = $oldbarcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': oldbarcode, 'picture': frodo, 'oldbarcode': barcode, 'cat': cat, 'tags': tags})
			db.update('products', where='barcode=$barcode', name=nam, description=found, barcode=bar, quantity=quant, picture=frodo, cat=ca, tags=tag, vars={'barcode':oldbarcode}, _test=debug)
			
			if oldbarcode != bar:
				#db.query('UPDATE `stats` SET `barcode` = $barcode WHERE `barcode` = $oldbarcode', vars={'barcode': oldbarcode, 'oldbarcode': bar})
				db.update('stats', where='barcode=$barcode', barcode=bar, vars={'barcode':oldbarcode}, _test=debug)
				#db.query('UPDATE `usage` SET `barcode` = $barcode WHERE `barcode` = $oldbarcode', vars={'barcode': oldbarcode, 'oldbarcode': bar})
				db.update('usage', where='barcode=$barcode', barcode=bar, vars={'barcode':oldbarcode}, _test=debug)
				
			db.query('INSERT INTO `usage` (`barcode`, `quantity`) VALUES ($barcode, $quantity)', vars={'quantity': quant, 'barcode': oldbarcode})
			#db.insert('usage', barcode=oldbarcode, quantity=str(quant), _test=debug)
			#name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode': oldbarcode})
			name = db.select('products', where='barcode=$barcode', vars={'barcode':oldbarcode}, _test=False)
			
			inform = name[0]
			inform['updated'] = 'true'
			inform['oldbarcode'] = bar
			inform['barcode'] = oldbarcode
			if spam:
				web.header('Content-Type', 'application/json')
			return json.dumps(inform)
		else:
			return json.dumps(['NS'])
		
	def deleteFun(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns
			A JSON object like: {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52, "thumb": "dog_thumb.png"}
		'''
		try: 
			wi = web.input()
			bar = wi['barcode']
		except:
			bar = kwargs['barcode']
		
		log = []
		vallog = []
		
		#name = db.query('SELECT * FROM `products` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		name = db.select('products', where='barcode=$barcode', vars={'barcode':bar}, _test=False)
		inform = name[0]
		
		#stated = db.query('SELECT * FROM `stats` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		stated = db.select('stats', where='barcode=$barcode', vars={'barcode':bar}, _test=False)
		stat = stated[0]
			
		#loged = db.query('SELECT `date`, `quantity` FROM `usage` WHERE `barcode` = $barcode', vars={'barcode':barcode})
		loged = db.select('usage', where='barcode=$barcode', vars={'barcode':bar}, _test=False, what='date,quantity')
		for x in range(len(loged)):
			vallog.append(loged[x])
			val = {'date': vallog[x]['date'].isoformat(' '), 'quantity': vallog[x]['quantity']}
			log.append(val)
		
		logSON = json.dumps(log)
		
		db.query('INSERT INTO `backup` (`id`, `barcode`, `name`, `description`, `quantity`, `cat`, `tags`, `picture`, `flag`, `last_5`, `all`, `log`) VALUES ($id, $barcode, $name, $description, $quantity, $cat, $tags, $picture, $flag, $last_5, $all, $log) ', vars={'barcode': inform['barcode'], 'name': inform['name'], 'quantity':inform['quantity'], 'id': inform['id'], 'description': inform['description'], 'quantity': inform['quantity'], 'cat': inform['cat'], 'tags': inform['tags'], 'picture': inform['picture'], 'flag': inform['flag'], 'last_5': stat['last_5'], 'all': stat['all'], 'log': logSON})
		
		db.query('DELETE FROM `products` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		db.query('DELETE FROM `stats` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		db.query('DELETE FROM `usage` WHERE `barcode` = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps(inform)
	
	def GET(self, bar):
		return self.getFunc(barcode=bar)
	
	@auth.oauth_protect
	def POST(self, bar):
		pass
	
	@auth.oauth_protect
	def PUT(self, bar):
		return self.putFunc(barcode=bar)
	
	@auth.oauth_protect
	def DELETE(self, bar):
		return self.deleteFunc(barcode=bar)
	
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		bar = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", bar
		
		if method == 'GET':
			#We just need the barcode since we're getting info about the product.
			got = self.getFunc(barcode=bar)
		if method == 'POST':
			#Doesn't do anything right now...
			#got = self.postFunc(barcode)
			print "Nothing to do, with FAIL"
		if method == 'PUT':
			#We have to get all the update info so make sure it's all passed...
			desc = kwargs['description']
			nam = kwargs['name']
			tag = kwargs['tags']
			ca = kwargs['cat']
			quant = kwargs['quantity']
			got = self.putFunc(barcode=bar, name=nam, description=desc, cat=ca, tags=tag, quantity=quant)
		if method == 'DELETE':
			#We just need the barcode for this one since it's just to delete the product...
			got = self.deleteFunc(barcode=bar)
			
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['barcode']
		
		print "Got back: ", got
		
		print "#########################################################"
		try:
			if answer == bar:
				print "%s: Passed" % str(method)
		except:
			print "%s: FAILED" % str(method)
		print "#########################################################"
		
		
class total:
	'''
	class documentation
	
	Returns and manipulates the total product database.
	'''
	def getFunc(self, **kwargs):
		'''
		function documentation
		
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			barcode - the products barcode
		Returns:
			A JSON object like: {"total" : [{"picture": "718103025027.png", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "barcode": "718103025027", "name": "Green Graph Composition", "flag": "M", "quantity": 1, "id": 3, "thumb": "718103025027_thumb.png"}, {"picture": "3037921120217.png", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "barcode": "3037921120217", "name": "Orange Graph Notebook", "flag": "L", "quantity": 1, "id": 4, "thumb": "3037921120217_thumb.png"}]}
		'''
		query = []
		name = db.query('SELECT * FROM `products`')
		for i in range(len(name)):
			query.append(name[i])
		if spam:
			web.header('Content-Type', 'application/json')
		return json.dumps({"total": query})
		
	def postFunc(self, **kwargs):
		'''
		function documentation
		
		POST verb call
		
		Args:
		Returns:
			A JSON object like: {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53}
	
		'''
		try:
			bobbins= web.input(picture={})
		except:
			bobbins = kwargs
			if 'picture' in bobbins: pass
			else: bobbins['picture'] = {}
		
		#if there is data in the Post go through the stuff to add it to the table if not, then let the client know there was no data sent...
		if bobbins['barcode'] and bobbins['name'] and bobbins['description'] and bobbins['quantity']:
			name = bobbins['name']
			barcode = bobbins['barcode']
			description = bobbins['description']
			quantity = bobbins['quantity']
			if 'cat' in bobbins: quantity = bobbins['cat']
			else: cat = 'None'
			if 'tags' in bobbins: quantity = bobbins['tags']
			else: cat = '["None"]'
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
			db.query('INSERT INTO `products` (`name`, `description`, `barcode`, `quantity`, `picture`, `cat`, `tags`) VALUES ($name, $description, $barcode, $quantity, $picture, $cat, $tags)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode, 'picture':frodo, 'cat': cat, 'tags': tags})
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
	
	def putFunc(self, **kwargs):
		'''
		function documentation
		
		PUT verb call
		
		Args:
		Returns:
		'''
		pass
		
	def deleteFun(self, **kwargs):
		'''
		function documentation
		
		DELETE verb call
		
		Args:
		Returns:
		'''
		pass
	
	def GET(self):
		'''
		function documentation
		
		Returns the given products info in JSON format
		
		Returns:
		'''
		return self.getFunc()
	
	@auth.oauth_protect
	def POST(self):
		'''
		function documentation
		
		Adds a new product
		
		Returns: 
		'''
		return self.postFunc()
	
	@auth.oauth_protect
	def PUT(self):
		'''
		function documentation
		
		Updates the current product according to the included data.
		
		Returns:
		'''
		pass
	
	@auth.oauth_protect
	def DELETE(self):
		'''
		function documentation
		
		Deletes the current product, and moves its data into the restore database.
		
		Returns: None
		'''
		pass
	
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		method = kwargs['method']
		
		print "Using method: ", method
		
		if method == 'GET':
			got = self.getFunc()
		if method == 'POST':
			bar = kwargs['barcode']
			desc = kwargs['description']
			nam = kwargs['name']
			newbar = kwargs['newbarcode']
			tag = kwargs['tags']
			ca = kwargs['cat']
			got = self.putFunc(barcode=bar, name=nam, description=desc, newbarcode=newbar, cat=ca, tags=tag)
		if method == 'PUT':
			#got = self.putFunc(bar)
			print "Not used in this call"
		if method == 'DELETE':
			#got = self.deleteFunc(bar)
			print "Not used in this call"
			
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		try:
			answer = answer_json['barcode']
		except:
			pass
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer_json:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"
		

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()