#!/usr/bin/python
import bluetooth

def find():
   for host, name in bluetooth.discover_devices(lookup_names=True):
      print host, name
      if (name == 'Josh ashby'):
         return host
      else:
         find()

def connect():
   services = bluetooth.find_service(address=host)
   for service in services:
      print service['name'], service['port']
      if service['name'] == 'SL4A':
         print 'true'
         port = service['port']
         print port
         return port

host = find()
port = connect()

print port, host

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

while True:
   print sock.recv(100)
