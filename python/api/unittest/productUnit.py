if __name__=="__main__":
	import os
	os.chdir('../')

	import sys
	abspath = os.getcwd()
	sys.path.append(abspath)
	os.chdir(abspath)
	
import json
import product

class infoTester(product.info):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Testing framework for the class, simply pass the info needed for each call.
		"""
		print "Testing calls from: %s" % __name__
		
		bar = kwargs['barcode']
		method = kwargs['method']
		
		print "Using method: ", method
		print "Using barcode: ", bar
		
		if method == 'GET':
			#We just need the barcode since we're getting info about the product.
			got = self.getFunc(barcode=bar)
		if method == 'POST':
			#Doesn't do anything right now...
			got = self.postFunc(barcode)
		if method == 'PUT':
			#We have to get all the update info so make sure it's all passed...
			#desc = kwargs['description']
			#nam = kwargs['name']
			#tag = kwargs['tags']
			#ca = kwargs['cat']
			quant = kwargs['quantity']
			got = self.putFunc(barcode=bar, quantity=quant)
		if method == 'DELETE':
			#We just need the barcode for this one since it's just to delete the product...
			got = self.deleteFunc(barcode=bar)
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if got:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		print "#########################################################"
	
	
class totalTester(product.total):
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
			bar = kwargs['barcode']
			desc = kwargs['description']
			nam = kwargs['name']
			tag = kwargs['tags']
			ca = kwargs['cat']
			quan = kwargs['quantity']
			got = self.postFunc(barcode=bar, name=nam, description=desc, cat=ca, tags=tag, quantity=quan)
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
	
	

unittestInfo = infoTester()
unittestTotal = totalTester()

unittestInfo.testFunc(method='GET', barcode='718103025027')

unittestInfo.testFunc(method='PUT', barcode='dog987', quantity='2')

unittestTotal.testFunc(method='GET')

tag = ['tv', 'electronics', 'media']
tag = json.dumps(tag)

unittestTotal.testFunc(method='POST', barcode='tv9', name='tv', description='A tv', cat='Electronics', tags=tag, quantity='6')

unittestInfo.testFunc(method='DELETE', barcode='tv9')
