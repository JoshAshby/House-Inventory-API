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
import tags
#import search

urls = (
	'/', 'index',
	#docu stuff...
	'/services/', 'calls',
	#admin stuff...
	'/admin', admin.app,
	#public stuff...
	'/product', product.app,
	'/category', cat.app,
	'/tags', tags.app,
	#'/search', search.app,
	#Test stuff...
	'/test', testPage.app
)
