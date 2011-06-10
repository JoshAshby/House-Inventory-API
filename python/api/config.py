#!/usr/bin/env python
import web

"""
Project Blue Ring
A scalable inventory control and management system based in the cloud.

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
"""

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='barcode')
        
urls = (
	'/', 'index',
	'/product/(.*)/info/', 'info',
	'/product/(.*)/delete/', 'delete',
	'/product/(.*)/log/', 'log',
	'/product/(.*)/stats/', 'stats',
	'/product/add/', 'add',
	'/product/update/', 'update',
	'/product/', 'total',
	'/product/names/', 'names'
)

render = web.template.render('/srv/http/template/')

#debug setter
spamandeggs = 0

#firefox debug setter (this is because firefox seems to want to download the json text instead of display it)...
'''set this to 1 for normal opperation, 0 for firefox...'''
spam = 0