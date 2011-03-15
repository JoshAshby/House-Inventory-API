#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
import request
import httplib, urllib
import threading
import Queue

debug = 0
version = ".01 alpha"

'''
python timer snippet, may use this for bluetooth device refresh...

        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.tabUpdate)
        timer.start(1000)
	
'''
port = 0

class bluetooth_tab(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		self.list = QtGui.QTreeWidget(self)
		self.list.setHeaderLabels(['Name', 'Host', 'Port'])
		
		self.refresh()
		
		fileBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox, 0)
		
		self.con_but = QtGui.QPushButton("Connect")
		self.ref_but = QtGui.QPushButton("Refresh")

		mainLayout.addWidget(self.list, 200)
		mainLayout.addWidget(self.con_but, 10)
		mainLayout.addWidget(self.ref_but, 10)
		
		self.connect(self.con_but, QtCore.SIGNAL("clicked()"),  self.connect_but)
		self.connect(self.ref_but, QtCore.SIGNAL("clicked()"),  self.refresh)
		
	def connect_but(self):
		data = self.list.currentItem()
		host = str(data.text(1))
		port = int(data.text(2))
		
		request.connect(host, port)
		
	def refresh(self):
		self.list.clear()
		host, name, port = request.find_host_GUI()
		
		if (name):
			item = QtGui.QTreeWidgetItem([name, host, port])
			self.list.addTopLevelItem(item)

class total_inventory(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		self.list = QtGui.QTreeWidget(self)
		self.list.setHeaderLabels(['Name', 'Description', 'Quantity', 'Flags'])
		
		params = urllib.urlencode({'type_of_query': 'total_inventory'})

		self.refresh()
		
		fileBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox, 0)

		mainLayout.addWidget(self.list, 200)
		
	def refresh(self):
		data = request.request(params)
		
		for i in range(len(data)):
			item = QtGui.QTreeWidgetItem([data[i]['name'], data[i]['description'], data[i]['quantity'] ])
			self.list.addTopLevelItem(item)
		

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		
		self.resize(800, 600)
		self.setWindowTitle('House Inventory')
		
		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setTabsClosable(True)
		self.mainTabWidget.setMovable(True)
		self.setCentralWidget(self.mainTabWidget)

		self.total_inventory_tab()
		self.bluetooth_tab()

		self.statusBar()
		
	def total_inventory_tab(self):
		new_inven = total_inventory(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Total Inventory")
		self.mainTabWidget.setCurrentIndex(newTab)
		
	def bluetooth_tab(self):
		new_inven = bluetooth_tab(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Bluetooth devices")
		self.mainTabWidget.setCurrentIndex(newTab)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())