if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)
	
import json
import order

class genTester(order.order):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		method = kwargs['method']
		
		print "Using method: ", method
		
		if method == 'GET':
			user = kwargs['user']
			ord = kwargs['order']
			got = self.getFunc(user=user, order = ord)
		if method == 'POST':
			got = self.postFunc()
		if method == 'PUT':
			got = self.putFunc()
		if method == 'DELETE':
			got = self.deleteFunc()
		
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if got:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"
		
if __name__=="__main__":
	unittestGen = genTester()
	ord = json.dumps({"3037921120217": 3})
	unittestGen.testFunc(method='GET', user="Josh", order=ord)