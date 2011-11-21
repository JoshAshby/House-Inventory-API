if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)
	
import hashlib

import account

class accountTester:
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		a = account.account()
		c = a.addUser(name='jow', passwd='new', email='geektechguy@gmail.com')
		print "adding: ", c
		print "logging in with password: ", a.loginPass('jow', 'new')
		print "logging out: ", a.logout('jow')
		print "check login: ", a.isLoged('jow')
		e = 'new'+str(c['salt'])
		d = hashlib.sha512(e).hexdigest()
		print d
		print c['hash']
		print type(d)
		print type(c['hash'])
		print d == c['hash']
		print "logging in with hash: ", a.loginHash('jow', d)
		print "check login: ", a.isLoged('jow')
		print "logging out: ", a.logout('jow')
		print "check login: ", a.isLoged('jow')
		print "change name: ", a.update('jow', name='joe')
		b = a.reset('joe')
		print "reset password: ", b
		print "logging in with new temp hash from reset: ", a.loginHash('joe', b['temp_hash'])
		print "oauth key gen: ", a.oauthKeys('joe')
		print "deleting user: ", a.delete('joe')