#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

import httplib, urllib
import sys

type_of_query = sys.argv[1]
params = urllib.urlencode({'type_of_query': type_of_query})

if (type_of_query != 'total_inventory') :
	query = sys.argv[2]
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query})

if (type_of_query =='update_product_quantity') :
	query = sys.argv[2]
	quantity = sys.argv[3]
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query, 'quantity': quantity})

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost")
conn.request("POST", "/barcode-perl-API/index.pl", params, headers)
response = conn.getresponse()
data = response.read()
print data
conn.close()
