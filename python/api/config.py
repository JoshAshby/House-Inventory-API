#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
Main app config file for URL's

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import web
import testPage
import cat
import admin
import product
#import tag
#import search

urls = (
	'/', 'index',
	#admin stuff...
	'/admin', admin.app,
	#'/product/(.*)/delete/', 'delete',
	#'/product/(.*)/restore/', 'restore',
	#'/product/(.*)/log/', 'log',
	#'/product/(.*)/stats/', 'stats',
	#'/product/add/', 'add',
	#'/product/update/', 'update',
	#public stuff...
	'/product', product.app,
	#'/product/(.*)/info/', 'info'
	#'/product/', 'total',
	#'/product/names/', 'names',
	'/category', cat.app,
	#'/category/(.*)/', 'cat_info',
	#'/category/', 'cat_total',
	#'/tag', tag.app,
	#'/search', search.app,
	'/test', testPage.app
)
