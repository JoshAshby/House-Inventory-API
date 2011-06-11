from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
register_openers()
datagen, headers = multipart_encode({"picture": open("add.png", "rb"), 'barcode': 'dog', 'name': 'god', 'description': 'dog', 'quantity': 5})
request = urllib2.Request("http://localhost/product/add/", datagen, headers)
print urllib2.urlopen(request).read()