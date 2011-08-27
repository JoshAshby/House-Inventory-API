#!/usr/bin env python
'''
Simple test script for adding a product to the database, including uploading a picture.

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
'''
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
register_openers()
datagen, headers = multipart_encode({"picture": open("add.png", "rb"), 'barcode': 'dog', 'name': 'god', 'description': 'dog', 'quantity': 5, 'picTrue': 1})
request = urllib2.Request("http://localhost/product/add/", datagen, headers)
print urllib2.urlopen(request).read()



import os
import sys
import json
import time
import oauth2
import urllib2
import datetime

account_inf = {}
account_inf['username'] = sys.argv[1]
account_inf['password'] = sys.argv[2]
account_inf['barcode'] = sys.argv[3]

BASE_URL = 'http://localhost/'

KEY    = 'rGgkUYhqjNEtwZdhnnLZoBkXkdKCPJmI'
SECRET = 'OSdTYJAeQJLLOHlOdmatRvEdBcuxuKGD'

HEADERS = {
  'User-Agent'    : 'Python-urllib/2.6 Tony Edition',
  'Accept'        : 'application/json',
}

LOGIN_URL  = BASE_URL + 'product/' +account_inf['barcode'] + '/log/'

def generate_oauth_request( method, url, parameters={} ):
	"""
	function documentation
	Generates an OAuth request to inclcude with the urllib2 requests for all admin functions.
	"""
	# Generate our Consumer object
	consumer = oauth2.Consumer( key = KEY, secret = SECRET )

	# Add parameters required by OAuth
	parameters['oauth_version']      = "1.0"
	parameters['oauth_nonce']        = oauth2.generate_nonce()
	parameters['oauth_timestamp']    = int(time.time())
	parameters['oauth_consumer_key'] = consumer.key

	# Generate and sign the request
	req = oauth2.Request( method = method, url = url, parameters = parameters )
	signature_method = oauth2.SignatureMethod_HMAC_SHA1()
	req.sign_request( signature_method, consumer, None )

	return req
  
def passStuff( account_info ):
	"""
	function documentation
	passes the OAuth and Account info off to the server and API
	"""
	parameters = {
		"username": account_info['username'],
		"password": account_info['password']
	}
	oauth = generate_oauth_request( 'POST', LOGIN_URL, parameters )
	req = urllib2.Request( LOGIN_URL, oauth.to_postdata(), headers=HEADERS )
	result = urllib2.urlopen( req ).read()
	json_result = json.loads( result )
	return json_result

if __name__ == "__main__":
	json = passStuff( account_inf )
	print json\