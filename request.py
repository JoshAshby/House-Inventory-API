#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

"""
Import all of the libraries we need.
httplib & urllib2 are used for the HTTP POST requests made to the API
sys is needed for the system arguments
bluetooth is for communicating with the phone which acts as a barcode scanner
json is to decrypt and encrypt variables in JSON format for interacting with the API
"""
import httplib, urllib
import sys
import bluetooth
import json

"""
sock is the socket for the bluetooth connection, all bluetooth functions happen through sock
"""
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

"""
as the user for which 
"""
API_host = raw_input("Please enter API host address: ")
if (API_host == ''):
	API_host = 'localhost'

"""
setup stuff for the HTTP requests. conn is the connection to the API that will be used, headers is what type of header gets sent so the server and script know what to do
"""
conn = httplib.HTTPConnection(API_host)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

"""
returns: host in the format of xx:xx:xx:xx:xx:xx
takes: nothing
finds device, this is going to be replaced with a GUI specific function in a little bit which will list return the host and name for a list widget
"""
def find_host():
	for host, name in bluetooth.discover_devices(lookup_names=True):
		if (name == 'Josh ashby' or host == '90:21:55:F8:9A:75'):
			return host

"""
returns: port number of SL4A, needed for connecting with the phone's python script inorder to get and pass data between the phone and computer
takes: host number in the format of xx:xx:xx:xx:xx:xx
finds which port everything, including the needed SL4A port, is running on. Needed in order to connect to device
"""
def find_port(host):
	services = bluetooth.find_service(address=host)
	for service in services:
		if service['name'] == 'SL4A':
			port = service['port']
			return port
	
"""
returns: nothing
takes: nothing
connect to the bluetooth device
"""
def connect(host, port):
	sock.connect((host, port))

"""
returns: 100bytes from bluetooth everytime it's called
takes: nothing
receive data from the bluetooth device
"""
def receive():
	return sock.recv(100)
	
"""
returns: nothing
takes: product_name, name of the product
send data to the bluetooth device
"""
def send(product_name):
	sock.send(product_name)

"""
returns: nothing
takes: nothing
take input from the bluetooth device and make requests to the API based off of barcode scanned
"""
def scan():
	while True:
		query = receive()
		params = urllib.urlencode({'type_of_query': 'single_product_info', 'query': query})
		data = request(params, query)

"""
returns: python array from decrypted JSON data
takes: params, urllib encoded query data
add a new product to the database incase the API returns no results for a product
"""
def add(params):
	conn.request("POST", "/barcode-perl-API/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	new_data = json.loads(data)
	#print new_data
	return new_data

"""
returns: python array or 'no_product' if the product does not exist (ie: API returns no results)
takes: params, a urllib encoded string
make a request to the API for data
"""
def request(params):
	conn.request("POST", "/perl/barcode/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	#print data
	if (data == ''):
		#new(query)
		return "no_product"
	else:
		new_data = json.loads(data)
		#print new_data['name']
		return new_data
	
"""
returns: nothing
takes: query, either barcode or name of a product
used for GUI interfacing to add a new product
"""
def newGUI(query):
	params = urllib.urlencode({'type_of_query': 'add_new_product', 'name': name, 'description': description, 'query': query, 'quantity': quantity})
	add(params)

"""
returns: nothing
takes: query, either barcode or name of a product
used only for command line interface
"""
def new(query):
	print "The product you scanned is not in the database, would you like to add it?"
	var = raw_input("Y/N: ")
	if (var == 'Y' or var == 'y' or var == 'yes'):
		name = raw_input("Enter Name: ")
		description = raw_input("Enter Description: ")
		quantity = raw_input("Enter Quantity: ")
		params = urllib.urlencode({'type_of_query': 'add_new_product', 'name': name, 'description': description, 'query': query, 'quantity': quantity})
		add(params)
	else:
		pass

"""
returns: python array decrypted from JSON data
takes: params, a urllib encoded string, and query, either barcode or name of a product
used only for command line
"""
def requestCMD(params, query):
	conn.request("POST", "/perl/barcode/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	#print data
	if (data == ''):
		new(query)
		#return "no_product"
	else:
		new_data = json.loads(data)
		#print new_data['name']
		return new_data

"""
returns: python variables, in the case of the API all data is returned as an array
takes: JSON formated data
decrypts the API's reponse which is in JSON to python variables
"""
def decrypt(json_data):
	decrypt_json = json.loads(json_data)
	return decrypt_json

"""
rest from here on out is just for command line input, which is only for debugging. Should be realitivly obvious whats happing here, just a bunch of if loops
"""
print "Types of querys: server\n total_inventory\n single_product_info\n update_product_quantity\n add_new_product"
type_of_query = raw_input("Please enter a query type or quit:")

if (type_of_query == 'server'):
	host = find_host()
	if (host == 'None'):
		host = find_host()
	port = find_port(host)
	connect(host,port)
	scan()

if (type_of_query == 'total_inventory') :
	params = urllib.urlencode({'type_of_query': type_of_query})
	request(params, type_of_query)

if (type_of_query == 'single_product_info') :
	query = raw_input("Name: ")
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query})
	request(params, query)

if (type_of_query =='update_product_quantity') :
	query = raw_input("Name: ")
	quantity = raw_input("Quantity: ")
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query, 'quantity': quantity})
	request(param, query)
	
if (type_of_query =='add_new_product') :
	name = raw_input("Name: ")
	description = raw_input("Description: ")
	quantity = raw_input("Quantity: ")
	host = find_host()
	if (host == 'None'):
		host = find_host()
	port = find_port(host)
	connect(host,port)
	query = receive()
	params = urllib.urlencode({'type_of_query': type_of_query, 'name': name, 'description': description, 'query': query, 'quantity': quantity})
	add(params)