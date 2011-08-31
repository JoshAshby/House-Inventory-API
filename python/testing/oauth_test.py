#!/usr/bin env python
'''
Simple test script for testing the oauth for the API

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com
'''
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

LOGIN_URL  = BASE_URL + 'test/'

def generate_oauth_request( method, url, parameters={} ):
	"""
	function documentation
	
	Generates an OAuth request to inclcude with the urllib2 requests for all admin functions.
	
	Args:
		method - The http request method. Default is POST.
		url - The URL to send the request to.
		parameters - A dict of various other parameters to include in the URL encoding.
	
	Returns:
		req - The signed OAuth request to use with urllib2
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
	
	Passes the OAuth and Account info off to the server and API.
	
	Args:
		account_info - A dictionary with the keys username and password.
		
	Returns:
		json_result - The JSON result of the request if successful.
		None - prints error to stdout if an error happens.
	"""
	
	parameters = {
		"username": account_info['username'],
		"password": account_info['password'],
		"barcode": account_info['barcode']
	}
	oauth = generate_oauth_request( 'PUT', LOGIN_URL, parameters )
	req = urllib2.Request( LOGIN_URL, oauth.to_postdata(), headers=HEADERS )
	req.get_method = lambda: 'PUT'
	try:
		result = urllib2.urlopen( req ).read()
		json_result = json.loads( result )
		return json_result
	except urllib2.HTTPError, e:
		print "Error: %s" %e
		return


if __name__ == "__main__":
	json = passStuff( account_inf )
	print json