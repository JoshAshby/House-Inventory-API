import web
import json
import re
import time
from rpy2.robjects import r
import rpy2.robjects as robj

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='pl_barcode')

query = []
log = []
quantity = []
date = []

name = db.query('SELECT quantity, date FROM stats WHERE barcode = $barcode ORDER BY date desc', vars={'barcode':'718103025027'})

for i in range(len(name)):
	query.append(name[i])

m = len(query)
for i in range(m):
	if (query[i]['quantity'] < query[i+1]['quantity']):
		quantity.append(int(query[i]['quantity']))
		date.append((query[0]['date'] - query[i]['date']).days)
	else:
		quantity.append(int(query[i]['quantity']))
		date.append((query[0]['date'] - query[i]['date']).days)
		break

robj.globalenv['quantity_y'] = robj.IntVector(quantity)
robj.globalenv['date_x'] = robj.IntVector(date)

lm = r['lm']('quantity_y ~cbind(date_x,(date_x)^2)')
lm.rx2('coefficients').rx2('(Intercept)')[0]