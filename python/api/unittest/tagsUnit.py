if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)

import json
import tags

class tagInfoTester(tags.tagsInfo):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Unit test for the test functions
		
		Should probably figure out how to work with the unittest2 lib for Python...
		Until then, this works fine...
		"""
		print "Testing calls from: %s" % __name__
		
		tags = kwargs['tag']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using tags: ", tags
		
		if method == 'GET':
			got = self.getFunc(tag=tags)
		if method == 'POST':
			got = self.postFunc(tag=tags)
		if method == 'PUT':
			got = self.putFunc(tag=tags)
		if method == 'DELETE':
			got = self.deleteFunc(tag=tags)
			
		answer_json = json.loads(got)
		
		answer = answer_json['products']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
			
		print "#########################################################"


class tagTotalTester(tags.tagsTotal):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Unit test for the test functions
		
		Should probably figure out how to work with the unittest2 lib for Python...
		Until then, this works fine...
		"""
		print "Testing calls from: %s" % __name__
		
		method = kwargs['method']
		
		print "Using method: ", method
		
		if method == 'GET':
			got = self.getFunc()
		if method == 'POST':
			got = self.postFunc()
		if method == 'PUT':
			got = self.putFunc()
		if method == 'DELETE':
			got = self.deleteFunc()
			
		answer_json = json.loads(got)
		
		answer = answer_json['tags']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"


tagInfoUnit = tagInfoTester()
tagTotalUnit = tagTotalTester()

tagInfoUnit.testFunc(method='GET', tag='paper')
tagTotalUnit.testFunc(method='GET')
