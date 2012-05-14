#!/usr/bin/env python2
"""
Project Blue Ring
An inventory control and management API
productDoc database document class

For more information, see: https://github.com/JoshAshby/House-Inventory-API

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import couchdbkit
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