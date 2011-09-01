import product

unittestInfo = product.info()
unittestTotal = product.total()

unittestInfo.testFunc(method='GET', barcode='dog987')
unittestInfo.testFunc(method='PUT', barcode='dog987', name='Dog', description='A dog of god', cat='Animal', tags='["Pet", "beagle"]', quantity='3')

unittestTotal.testFunc(method='GET')
