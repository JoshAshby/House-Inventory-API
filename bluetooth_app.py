#!/usr/bin/python
import bluetooth

def find_host():
	for host, name in bluetooth.discover_devices(lookup_names=True):
		print host, name
		if (name == 'Josh ashby' or host == '90:21:55:F8:9A:75'):
			return host

def find_port(host):
	services = bluetooth.find_service(address=host)
	for service in services:
		print service['name'], service['port']
		if service['name'] == 'SL4A':
			port = service['port']
			return port
	
def connect(host, port):
	sock.connect((host, port))

def receive():
	return sock.recv(100)
	
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
host = find_host()
print host
port = find_port(host)
print host, port
connect(host,port)

while True:
	print receive()