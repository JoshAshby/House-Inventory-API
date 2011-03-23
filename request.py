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
setup stuff for the HTTP requests. conn is the connection to the API that will be used, headers is what type of header gets sent so the server and script know what to do
"""
API_host = "localhost"
conn = httplib.HTTPConnection(API_host)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

"""
returns: strings: host in the format of xx:xx:xx:xx:xx:xx, name and port number of the SL4A service as a number
takes: nothing
finds device, GUI use
"""
def find_host_GUI():
	for host, name in bluetooth.discover_devices(lookup_names=True):
		if (host):
			services = bluetooth.find_service(address=host)
			for service in services:
				if (service['name'] == 'SL4A'):
					port = service['port']
					if (port):
						return host, name, port
					else:
						return 'None', 'None', 'None'
		else:
			return 'None', 'None', 'None'
	
"""
returns: nothing
takes: nothing
connect to the bluetooth device
"""
def connect(host, port):
	#sock.close()
	sock.connect((host, port))
	
"""
returns: 100bytes from bluetooth everytime it's called
takes: nothing
receive data from the bluetooth device
"""
def receive():
	data = sock.recv(100)
	return data
	
"""
returns: nothing
takes: product_name, name of the product
send data to the bluetooth device
"""
def send(product_name):
	sock.send(product_name)

"""
returns: python array or 'no_product' if the product does not exist (ie: API returns no results)
takes: params, a urllib encoded string
make a request to the API for data
"""
def request(params):
	conn.request("POST", "/perl/OO/api.pl", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	if (data == ''):
		return "no_product"
	else:
		new_data = json.loads(data)
		return new_data

"""
returns: python variables, in the case of the API all data is returned as an array
takes: JSON formated data
decrypts the API's reponse which is in JSON to python variables
"""
def decrypt(json_data):
	decrypt_json = json.loads(json_data)
	return decrypt_json