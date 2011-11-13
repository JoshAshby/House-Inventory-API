#!/usr/bin/env python2
import os
os.chdir('../')

import sys
abspath = os.getcwd()
sys.path.append(abspath)
os.chdir(abspath)

import json

from productUnit import *
from catUnit import *
from tagsUnit import *
from logUnit import *
from accountUnit import *

unittestInfo = infoTester()
unittestTotal = totalTester()
unittestCatInfo = catInfoTester()
unittestCatTotal = catTotalTester()
unittestCatTag = catTagTester()
unittestLog = logTester()
tagInfoUnit = tagInfoTester()
tagTotalUnit = tagTotalTester()
unittestAccount = accountTester()

try:
	if sys.argv[1] == 'GET':
		if sys.argv[2] == 'info':
			bar = sys.argv[3]
			unittestInfo.testFunc(method='GET', barcode=bar)
			
		if sys.argv[2] == 'total':
			unittestTotal.testFunc(method='GET')
			
		if sys.argv[2] == 'catinfo':
			cat = sys.argv[3]
			unittestCatInfo.testFunc(method='GET', category=cat)
			
		if sys.argv[2] == 'cattotal':
			unittestCatTotal.testFunc(method='GET')
			
		if sys.argv[2] == 'cattag':
			cat = sys.argv[3]
			tag = sys.argv[4]
			unittestCatTag.testFunc(method='GET', category=cat, tag=tag)
			
		if sys.argv[2] == 'log':
			bar = sys.argv[3]
			unittestLog.testFunc(method='GET', barcode=bar)
			
		if sys.argv[2] == 'tag':
			tag = sys.argv[3]
			tagInfoUnit.testFunc(method='GET', tag=tag)
			
		if sys.argv[2] == 'tagtotal':
			tagTotalUnit.testFunc(method='GET')
		
	if sys.argv[1] == 'POST':
		#tag = ['tv', 'electronics', 'media']
		#tag = json.dumps(tag)
		
		barcode = sys.argv[2]
		name = sys.argv[3]
		description = sys.argv[4]
		cat = sys.argv[5]
		quantity = sys.argv[6]
		tag = json.dumps(sys.argv[7])

		unittestTotal.testFunc(method='POST', barcode='tv9', name='tv', description='A tv', cat='Electronics', tags=tag, quantity='6')
		
	if sys.argv[1] == 'PUT':
		bar = sys.argv[2]
		quant = int(sys.argv[3])
		unittestInfo.testFunc(method='PUT', barcode=bar, quantity=quant)
		
	if sys.argv[1] == 'DELETE':
		bar = sys.argv[2]
		unittestInfo.testFunc(method='DELETE', barcode=bar)
		
except:
	pass
	'''
	unittestInfo.testFunc(method='GET', barcode='718103025027')

	unittestInfo.testFunc(method='PUT', barcode='3037921120217', quantity=8)

	unittestTotal.testFunc(method='GET')

	tag = ['tv', 'electronics', 'media']
	tag = json.dumps(tag)

	unittestTotal.testFunc(method='POST', barcode='tv9', name='tv', description='A tv', cat='Electronics', tags=tag, quantity='6')

	unittestInfo.testFunc(method='DELETE', barcode='tv9')

	unittestCatInfo.testFunc(method='GET', category='Animal')

	unittestCatTotal.testFunc(method='GET')

	unittestCatTag.testFunc(method='GET', category='Notebook', tag='paper')

	tagInfoUnit.testFunc(method='GET', tag='paper')
	tagTotalUnit.testFunc(method='GET')

	unittestLog.testFunc(method='GET', barcode='dog987')

	unittestAccount.testFunc()
	'''