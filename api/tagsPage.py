#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Tags sub-app for handeling all tag API calls...

Neat thing about tags is multiple tags can apply to a product, and it helps you narrow down with categories.
Even though tags act a lot like categories at first, the fact that you can look at a category, then find only a certian tag with in that category is really
powerful.

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import json
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
from productDocument import *
import tagView
import baseObject

baseObject.urlReset()


@baseObject.route('/(.*)/')
class tagsInfo(baseObject.baseHTTPObject):
	'''
	Returns all the products in a tag
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
		'''
		self.members(*args, **kwargs)
		tag = self.hasMember('tag')
		
		query = database.view("cattag/tags", key=tag).all()
		
		for i in range(len(query)):
			query[i] = query[i]['value']
			
		query = {'data': query}
		
		view = tagView.infoView(data=query)
		
		return view.returnData()


@baseObject.route('/')
class tagsTotal(baseObject.baseHTTPObject):
	'''
	Returns all the tags.
	'''
	def get(self, *args, **kwargs):	
		'''
		GET verb call
		
		Returns:
			A JSON object like: {"tags" : ["abc", "def"]}
		'''
		dog = []
		query = database.view("products/admin").all()
		
		for x in range(len(query)):
			for z in range(len(query[x]['value']['tags'])):
				dog.append(query[x]['value']['tags'][z])
		
		queryFix = list(set(dog))
		
		queryFinal = {'data': queryFix}
		
		view = tagView.totalView(data=queryFinal)
		
		return view.returnData()
		

app = web.application(baseObject.urls, globals())
