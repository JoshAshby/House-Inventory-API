#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

import httplib, urllib
import sys
import bluetooth

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

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
	

def scan():
	while True:
		query = receive()
		params = urllib.urlencode({'type_of_query': 'single_product_info', 'query': query})
		request(params)

def request(params):
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = httplib.HTTPConnection("localhost")
	conn.request("POST", "/barcode-perl-API/test.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	print data
	conn.close()

type_of_query = sys.argv[1]

if (type_of_query == 'server'):
	host = find_host()
	if (host == 'None'):
		host = find_host()
	port = find_port(host)
	connect(host,port)
	scan()
else:
	params = urllib.urlencode({'type_of_query': type_of_query})
	request(params)

if (type_of_query == 'total_inventory') :
	params = urllib.urlencode({'type_of_query': type_of_query})
	request(params)

if (type_of_query == 'single_product_info') :
	query = sys.argv[2]
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query})
	request(params)

if (type_of_query =='update_product_quantity') :
	query = sys.argv[2]
	quantity = sys.argv[3]
	params = urllib.urlencode({'type_of_query': type_of_query, 'query': query, 'quantity': quantity})
	request(params)