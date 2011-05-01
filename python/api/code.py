import web

db = web.database(dbn='mysql', user='root', pw='speeddyy5', db='pl_barcode')
        
urls = (
	'/', 'index',
	'/product/info/(.*)', 'info'
)

render = web.template.render('/srv/http/template/')

class index:        
	def GET(self):
		return render.index()

class info:
	def GET(self, query):
		name = db.query("SELECT * FROM products WHERE barcode = $id", vars={'id':query})
		inform = name[0]
		return render.info(inform['name'], inform['barcode'])
		
if __name__ == "__main__":
	app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()