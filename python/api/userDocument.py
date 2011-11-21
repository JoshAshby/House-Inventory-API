#!/usr/bin/env python
"""
Project Blue Ring
An inventory control and management API
productDoc database document class

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""
import couchdbkit

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

class userDoc(couchdbkit.Document):
	username = couchdbkit.StringProperty()
	hash = couchdbkit.StringProperty()
	permission = couchdbkit.StringProperty()
	ip = couchdbkit.StringProperty()
	datetime = couchdbkit.StringProperty()
	password = couchdbkit.StringProperty()
	salt = couchdbkit.StringProperty()
	email = couchdbkit.StringProperty()
	
	doc_type = "userDoc"
	
	logged_in = couchdbkit.BooleanProperty()
	
	oauth = couchdbkit.DictProperty()

userDoc.set_db(database)