import cat

unittestCatInfo = cat.catInfo()
unittestCatTotal = cat.catTotal()
unittestCatTag = cat.catTag()

unittestCatInfo.testFunc(method='GET', category='Other')

unittestCatTotal.testFunc(method='GET')

unittestCatTag.testFunc(method='GET', category='Other', tag='paper')