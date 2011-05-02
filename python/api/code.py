import web
import json
import re

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='pl_barcode')
        
urls = (
	'/', 'index',
	'/product/(.*)/info/', 'info',
	'/product/(.*)/delete/', 'delete',
	'/product/(.*)/(.*)/(.*)/(.*)/add/', 'add',
	'/product/(.*)/(.*)/(.*)/(.*)/update/', 'update',
	'/product/', 'total',
	'/product/names/', 'names',
	'/product/(.*)/log/', 'log',
	'/product/(.*)/stats/', 'stats',
	'/product/(.*)/log/flot/', 'log_flot',
	'/product/(.*)/stats/flot/', 'stats_flot'
)

render = web.template.render('/srv/http/template/')

class index:        
	def GET(self):
		return render.index()

class info:
	def GET(self, barcode):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class total:
	def GET(self):
		query = []
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i])
		web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class add:
	def GET(self, barcode, name, quantity, description):
		p = re.compile('\+')
		found = p.sub( ' ', description)
		db.query('INSERT INTO products (name, description, barcode, quantity) VALUES ($name, $description, $barcode, $quantity)', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['added'] = 'true'
		db.query('INSERT INTO stats (barcode, quantity) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)
		
class update:
	def GET(self, barcode, name, quantity, description):
		p = re.compile('\+')
		found = p.sub( ' ', description)
		db.query('UPDATE products SET name = $name, description = $description, barcode = $barcode, quantity = $quantity WHERE barcode = $barcode', vars={'name': name, 'description': found, 'quantity': quantity , 'barcode': barcode})
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		inform['updated'] = 'true'
		db.query('INSERT INTO stats (barcode, quantity) VALUES ($barcode, $quantity)', vars={'quantity': quantity , 'barcode': barcode})
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class delete:
	def GET(self, barcode):
		name = db.query('SELECT * FROM products WHERE barcode = $barcode', vars={'barcode':barcode})
		inform = name[0]
		db.query('DELETE FROM products WHERE barcode = $barcode', vars={'barcode': barcode})
		inform['deleted'] = 'true'
		web.header('Content-Type', 'application/json')
		return json.dumps(inform)

class names:
	def GET(self):
		query = []
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i]['name'])
		name = db.query('SELECT * FROM products')
		for i in range(len(name)):
			query.append(name[i]['barcode'])
		web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
class log:
	def GET(self, barcode):
		query = []
		name = db.query('SELECT quantity, date FROM stats WHERE barcode = $barcode', vars={'barcode':barcode})
		for i in range(len(name)):
			query.append(name[i])
		for i in range(len(query)):
			query[i]['date'] = query[i]['date'].isoformat(' ')
		web.header('Content-Type', 'application/json')
		return json.dumps(query)
		
if __name__ == "__main__":
	app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()