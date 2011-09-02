import json
import stats

class statsTester(stats.stats):
	def testFunc(self, **kwargs):
		"""
		function documentation
		
		Unit test
		
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
		
		answer = answer_json['predicted']
		
		print "Got back: ", got
		
		print "#########################################################"
		
		if answer:
			print "%s: Passed" % str(method)
		else:
			print "%s: FAILED" % str(method)
		
		print "#########################################################"

unittestStats = statsTester()

unittestStats.testFunc(method='GET', barcode='dog987')