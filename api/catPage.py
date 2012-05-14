#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Category sub-app for handeling all category API calls...

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import couchdbkit
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
from productDocument import *
import catView
import baseObject

baseObject.urlReset()


@baseObject.route('/')
class catTotal(baseObject.baseHTTPObject):
	'''
	Category maniplulation object
	'''	
	def get(self, *args, **kwargs):
		'''
		GET verb call
		
		Args:
		Returns:
		'''
		query = []
		name = database.view("products/admin").all()
		
		for i in range(len(name)):
			query.append(name[i]['value']['category'])
		
		
		queryFix = list(set(query))
		
		names = {'data': queryFix}
		
		view = catView.totalView(data=names)
		
		return view.returnData()


@baseObject.route('/(.*)/')
class catInfo(baseObject.baseHTTPObject):
	'''
	Category maniplulation object
	'''
	def get(self, *args, **kwargs):
		'''
		GET verb call
		
		Returns the info on the product in JSON form.
		
		Args:
			cat - the cateogry
		Returns:
		'''
		self.members(*args, **kwargs)
		cat = self.hasMember('category')
			
		query = database.view("cattag/categorys", key=cat).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
		
		totals = {'data': query}
		
		view = catView.infoView(data=totals)
		
		return view.returnData()

		

@baseObject.route('/(.*)/tag/(.*)/')
class catTag(baseObject.baseHTTPObject):
	'''
	Category maniplulation object
	'''
	def get(self, *args, **kwargs):
		'''
		GET verb call
		
		Args:
		Returns:
		'''
		self.members(*args, **kwargs)
		cat = self.hasMember('category')
		tag = self.hasMember('tag')
		if tag == cat: tag = self.hasMember(2)
			
		query = []
		dog = []
		
		query = database.view("cattag/categorys", key=cat).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
		
		for x in range(len(query)):
			e = query[x]['tags']
			for z in range(len(e)):
				if e[z] == tag:
					dog.append(query[x])
				else: pass
		
		dog = {'data': dog}
		
		view = catView.tagView(data=dog)
		
		return view.returnData()
		

app = web.application(baseObject.urls, globals())