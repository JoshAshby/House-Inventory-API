#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
import request
import httplib, urllib

debug = 0
version = ".01 alpha"

'''
python timer snippet, may use this for bluetooth device refresh...

        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.tabUpdate)
        timer.start(1000)
	
'''

class total_inventory(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		self.list = QtGui.QTreeWidget(self)
		self.list.setHeaderLabels(['Name', 'Description', 'Quantity'])
		
		params = urllib.urlencode({'type_of_query': 'total_inventory'})

		data = request.request(params)
		print data
		
		for i in range(len(data)):
			item = QtGui.QTreeWidgetItem([data[i]['name'], data[i]['description'], data[i]['quantity'] ])
			self.list.addTopLevelItem(item)
		
		fileBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox, 0)

		mainLayout.addWidget(self.list, 200)
		

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setTabsClosable(True)
		self.mainTabWidget.setMovable(True)
		self.setCentralWidget(self.mainTabWidget)

		self.total_inventory_tab()

		self.statusBar()
		
	def total_inventory_tab(self):
		new_inven = total_inventory(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Total Inventory")
		self.mainTabWidget.setCurrentIndex(newTab)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())