#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

import httplib, urllib
import sys

type_of_query = sys.argv[1]
query = sys.argv[2]

params = urllib.urlencode({'type_of_query': type_of_query, 'query': query})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost")
conn.request("POST", "/barcode-perl-API/index.pl", params, headers)
response = conn.getresponse()
data = response.read()
print data
conn.close()
