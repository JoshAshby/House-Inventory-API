if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)

import account
a = account.account()
print "adding: ", a.addUser(name='jow', passwd='new', email='geektechguy@gmail.com')
print "logging in with password: ", a.loginPass('jow', 'new')
print "logging out: ", a.logout('jow')
print "check login: ", a.isLoged('jow')
print "change name: ", a.update('jow', name='joe')
b = a.reset('joe')
print "reset password: ", b
print "logging in with new temp hash from reset: ", a.loginHash('joe', b['temp_hash'])
print "deleting user: ", a.delete('joe')

