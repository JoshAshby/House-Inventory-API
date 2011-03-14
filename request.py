#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

import httplib, urllib
import sys
import bluetooth
import virtkey
import json

last_query = 0

y = 0

v = virtkey.virtkey()
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

API_host = raw_input("Please enter API host address: ")
if (API_host == ''):
	API_host = 'localhost'
	
conn = httplib.HTTPConnection(API_host)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

def find_host():
	for host, name in bluetooth.discover_devices(lookup_names=True):
		if (name == 'Josh ashby' or host == '90:21:55:F8:9A:75'):
			return host

def find_port(host):
	services = bluetooth.find_service(address=host)
	for service in services:
		if service['name'] == 'SL4A':
			port = service['port']
			return port
	
def connect(host, port):
	sock.connect((host, port))

def receive():
	return sock.recv(100)
	
def send(product_name):
	sock.send(product_name)
	
def scan():
	while True:
		query = receive()
		params = urllib.urlencode({'type_of_query': 'single_product_info', 'query': query})
		data = request(params, query)
		if (y):
			for x in query:
				v.press_unicode(ord(x))
				v.release_unicode(ord(x))

def add(params):
	conn.request("POST", "/barcode-perl-API/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	new_data = json.loads(data)
	print new_data

def request(params, query):
	conn.request("POST", "/barcode-perl-API/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	print data
	if (data == ''):
		new(query)
	else:
		new_data = json.loads(data)
		print new_data
	
def new(query):
	print "The product you scanned is not in the database, would you like to add it?"
	var = raw_input("Y/N: ")
	if (var == 'Y'):
		name = raw_input("Enter Name: ")
		description = raw_input("Enter Description: ")
		quantity = raw_input("Enter Quantity: ")
		params = urllib.urlencode({'type_of_query': 'add_new_product', 'name': name, 'description': description, 'query': query, 'quantity': quantity})
		add(params)
			
def decrypt(json_data):
	decrypt_json = json.loads(json_data)
	return decrypt_json

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
	request(params)

if (type_of_query == 'single_product_info') :
	query = raw_input("Name: ")
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query})
	request(params)

if (type_of_query =='update_product_quantity') :
	query = raw_input("Name: ")
	quantity = raw_input("Quantity: ")
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query, 'quantity': quantity})
	request(params)
	
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