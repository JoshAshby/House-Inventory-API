try:
 from cStringIO import StringIO
except ImportError:
 from StringIO import StringIO

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import couchdbkit
import datetime

buffer = StringIO()

matplotlib.use('Agg')

databaseName = 'stats'
database = couchdbkit.Server()[databaseName]

class productDoc(couchdbkit.Document):
 barcode = couchdbkit.StringProperty()

class userDoc(couchdbkit.Document):
 username = couchdbkit.StringProperty()

productDoc.set_db(database)
userDoc.set_db(database)

fig = plt.figure()
ax = fig.add_subplot(111)

product = productDoc.view("products/admin", key="3037921120217").first()

a = product.log

query = sorted(a, key=lambda a: a['date'], reverse=True)

date = []
quantity = []

for key in range(len(query)):
 date.append(datetime.datetime.strptime(query[key]['date'], '%Y-%m-%d %H:%M:%S'))
 quantity.append(query[key]['quantity'])

ax.plot(date, quantity)

ax.xaxis.set_major_locator( MonthLocator() )
ax.xaxis.set_major_formatter( DateFormatter('%m-%Y') )

ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()

fig.savefig(buffer)

graph = buffer.getvalue()
buffer.close()

f = open("test.png", "wr")
f.write(graph)
f.close()