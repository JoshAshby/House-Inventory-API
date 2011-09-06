if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)
	
import testPage
import json

class tester(testPage.test):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Unit test for the test functions
		
		Should probably figure out how to work with the unittest2 lib for Python...
		Until then, this works fine...
		"""
		print "Testing calls from: %s" % __name__
		
		bar = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", bar
		
		if method == 'GET':
			got = self.getFunc(barcode=bar)
		if method == 'POST':
			got = self.postFunc(barcode=bar)
		if method == 'PUT':
			got = self.putFunc(barcode=bar)
		if method == 'DELETE':
			got = self.deleteFunc(barcode=bar)
			
		answer_json = json.loads(got)
		
		answer = answer_json['barcode']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		try:
			if answer == bar:
				print "%s: Passed" % str(method)
		except:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"

#testUnit = testPage.test()
testUnit = tester()
testUnit.testFunc(method='GET', barcode='718103025027')
