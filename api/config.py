#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
Main app config file for URL's

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
from configSub import *
import web
import testPage
import catPage
import productPage
import tagsPage
import logPage
import graphPage
import orderPage

base = '/bluering/'

urls = (
	(base + 'product'), product.app,
	(base + 'category'), cat.app,
	(base + 'tag'), tags.app,
	(base + 'log'), log.app,
	(base + 'graph'), graph.app,
	(base + 'order'), order.app,
	(base + 'test'), testPage.app
)
