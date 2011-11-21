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
try:
	from configSub import *
except:
	import sys, os
	abspath = os.path.dirname(__file__)
	sys.path.append(abspath)
	os.chdir(abspath)
from configSub import *
import web
import testPage
import cat
import product
import tags
import log
import graph

urls = (
	'/', 'index',
	'/product', product.app,
	'/category', cat.app,
	'/tag', tags.app,
	'/log', log.app,
	'/graph', graph.app,
	#Test stuff...
	'/test', testPage.app
)
