import web
import json
import re

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='pl_barcode')
        
urls = (
	'/', 'index',
	'/product/info/(.*)', 'info',
	'/product/delete/(.*)', 'delete',
	'/product/add/(.*)/(.*)/(.*)/(.*)', 'add',
	'/product/update/(.*)/(.*)/(.*)/(.*)', 'update',
	'/total/', 'total',
	'/names/', 'names',
	'/log/(.*)', 'log',
	'/stats/(.*)', 'stats',
	'/log/flot/(.*)', 'log_flot',
	'/stats/flot/(.*)', 'stats_flot'
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
		
if __name__ == "__main__":
	app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()