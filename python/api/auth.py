#!/usr/bin/env python

"""
Project Blue Ring
An inventory control and management API
OAuth snippet

http://xkcd.com/353/

Josh Ashby
2011
http://joshashby.com
joshuaashby@joshashby.com

Snippet taken from/adapted from: https://github.com/DaGoodBoy/webpy-example/blob/master/lib/wpauth.py
"""
import web
import oauth2
import string
import account as acc

UNAUTHORIZED_MESSAGE = 'You are not authorized to access this content'
UNAUTHORIZED_HEADERS = { 'WWW-Authenticate' : 'Basic realm="Blue Ring"' }

def split_header( header ):
	"""
	Turn Authorization: header into parameters.
	"""
	
	params = {}
	parts = header.split(',')
	for param in parts:
		# Ignore realm parameter.
		if param.find('realm') > -1:
			continue
		param = param.strip()
		# Split key-value.
		param_parts = param.split('=', 1)
		# Remove quotes and unescape the value.
		params[param_parts[0]] = urllib.unquote(param_parts[1].strip('\"'))
	return params


def validate_two_leg_oauth():
	"""
	Verify 2-legged oauth request using values in "Authorization" header.
	"""
	
	parameters = web.input()
	#print parameters
	if web.ctx.env.has_key('HTTP_AUTHORIZATION') and web.ctx.env['HTTP_AUTHORIZATION'].startswith('OAuth '):
		parameters = split_header( web.ctx.env['HTTP_AUTHORIZATION'] )

	# We have to reconstruct the original full URL used when signing
	# so if there are ever 401 errors verifying a request, look here first.
	req = oauth2.Request( web.ctx.env['REQUEST_METHOD'],
		web.ctx['homedomain'] + web.ctx.env['REQUEST_URI'],
		parameters = parameters )

	if not req.has_key('oauth_consumer_key'):
		print "wrong"
		raise web.unauthorized()
	#print req
	# Verify the account referenced in the request is valid
	accoun = acc.account()
	account = accoun.findByKey(req['oauth_consumer_key'])
	if not account:
		print "ops"
		raise web.unauthorized( UNAUTHORIZED_MESSAGE )

	# Create an oauth2 Consumer with an account's consumer_key and consumer_secret
	# to be used to verify the request
	#consumer = oauth2.Consumer('rGgkUYhqjNEtwZdhnnLZoBkXkdKCPJmI', 'OSdTYJAeQJLLOHlOdmatRvEdBcuxuKGD')
	consumer = oauth2.Consumer(account['shared'], account['secret'])

	# Create our oauth2 Server and add hmac-sha1 signature method
	server = oauth2.Server()
	server.add_signature_method( oauth2.SignatureMethod_HMAC_SHA1() )
	
	# Attempt to verify the authorization request via oauth2
	try:
		server.verify_request( req, consumer, None )
	except oauth2.Error, e:
		print "fail"
		print '%s %s' % ( repr(e), str(e) )
		raise web.unauthorized( e )
	except KeyError, e:
		print "ugh"
		raise web.unauthorized( "You failed to supply the necessary parameters (%s) to properly authenticate " % e )
	except Exception, e:
		print "bug"
		raise web.unauthorized( repr(e) + ' ' + str(e) )

	return True


def oauth_protect(target):
	"""
	This is the decorator to validate oauth authentication
	
	Use by placing an
		``@auth.oauth_protect``
	before the function def.
	"""
	
	def decorated_function( *args, **kwargs ):
		validate_two_leg_oauth()
		return target( *args, **kwargs )
		
	return decorated_function