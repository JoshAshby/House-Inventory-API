if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)
	
import json
import cat

class catInfoTester(cat.catInfo):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		cat = kwargs['category']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using category: ", cat
		
		if method == 'GET':
			got = self.getFunc(category=cat)
		if method == 'POST':
			got = self.postFunc(category=cat)
		if method == 'PUT':
			got = self.putFunc(category=cat)
		if method == 'DELETE':
			got = self.deleteFunc(category=cat)
		
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['products']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"
		

class catTotalTester(cat.catTotal):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
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
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['categories']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"


class catTagTester(cat.catTag):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		cat = kwargs['category']
		tags = kwargs['tag']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using category: ", cat
		print "Using tag: ", tags
		
		if method == 'GET':
			got = self.getFunc(category=cat, tag=tags)
		if method == 'POST':
			got = self.postFunc(category=cat, tag=tags)
		if method == 'PUT':
			got = self.putFunc(category=cat, tag=tags)
		if method == 'DELETE':
			got = self.deleteFunc(category=cat, tag=tags)
		
		answer_json = json.loads(got)
		
		#this is just a copy from the test class, needs to be updated for each method...
		answer = answer_json['products']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"


unittestCatInfo = catInfoTester()
unittestCatTotal = catTotalTester()
unittestCatTag = catTagTester()

unittestCatInfo.testFunc(method='GET', category='Animal')

unittestCatTotal.testFunc(method='GET')

unittestCatTag.testFunc(method='GET', category='Notebook', tag='paper')