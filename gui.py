#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
import request
import httplib, urllib
import threading
import Queue

debug = 0
version = ".5 alpha"

class bluetooth_tab(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		self.list = QtGui.QTreeWidget(self)
		self.list.setHeaderLabels(['Name', 'Host', 'Port'])
		
		fileBox = QtGui.QHBoxLayout()
		buttonBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox, 0)
		
		self.con_but = QtGui.QPushButton("Connect")
		self.ref_but = QtGui.QPushButton("Refresh")

		mainLayout.addWidget(self.list)
		fileBox.addLayout(buttonBox)
		buttonBox.addWidget(self.con_but)
		buttonBox.addWidget(self.ref_but)
		
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
			item = QtGui.QTreeWidgetItem([name, host, str(port)])
			self.list.addTopLevelItem(item)

class add_product(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		fileBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox)
		formBox = QtGui.QFormLayout()
		fileBox.addLayout(formBox)
		
		self.product_name = QtGui.QLineEdit()
		self.product_barcode = QtGui.QLineEdit()
		self.product_description = QtGui.QPlainTextEdit()
		self.product_quantity = QtGui.QLineEdit()
		self.product_flag = QtGui.QComboBox()
		
		self.product_flag.addItems(['L', 'M', 'H'])
		
		self.submit = QtGui.QPushButton("Add New Product")
		
		formBox.addRow(self.tr("Name: "), self.product_name)
		formBox.addRow(self.tr("Barcode: "), self.product_barcode)
		formBox.addRow(self.tr("Description: "), self.product_description)
		formBox.addRow(self.tr("Quantity: "), self.product_quantity)
		formBox.addRow(self.tr("Flag: "), self.product_flag)
		formBox.addRow(self.tr("Submit Product Info Addition? "), self.submit)
		
		self.connect(self.submit, QtCore.SIGNAL("clicked()"), self.product_add)
		
	def product_add(self):
		name = self.product_name.text()
		barcode = self.product_barcode.text()
		description = self.product_description.toPlainText()
		quantity = self.product_quantity.text()
		flag = self.product_flag.currentText()
		
		if (barcode):
			params = urllib.urlencode({'type_of_query': 'add_new_product',  'name': name, 'description': description, 'query': barcode, 'quantity': quantity, 'flag': flag})
			data = request.request(params)
			
			self.product_name.clear()
			self.product_barcode.clear()
			self.product_description.clear()
			self.product_quantity.clear()

class total_inventory(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)
		mainLayout.setSpacing(0)
		self.setLayout(mainLayout)
		
		self.list = QtGui.QTreeWidget(self)
		self.list.setHeaderLabels(['Name', 'Description', 'Quantity', 'Barcode', 'Flags'])

		self.refresh()
		
		fileBox = QtGui.QHBoxLayout()
		mainLayout.addLayout(fileBox)
		formBox = QtGui.QFormLayout()
		fileBox.addLayout(formBox)
		
		self.product_name = QtGui.QLineEdit()
		self.product_name.setReadOnly(True)
		self.product_barcode = QtGui.QLineEdit()
		self.product_barcode.setReadOnly(True)
		self.product_description = QtGui.QPlainTextEdit()
		self.product_description.setReadOnly(True)
		self.product_quantity = QtGui.QLineEdit()
		self.product_quantity.setReadOnly(True)
		
		self.edit = QtGui.QPushButton("Edit")
		self.submit = QtGui.QPushButton("Submit Changes")
		self.submit.setEnabled(False)
		self.delete = QtGui.QPushButton("Delete Product")
		self.delete.setEnabled(False)
		self.ref_but = QtGui.QPushButton("Refresh Table")
		
		formBox.addRow(self.tr("Name: "), self.product_name)
		formBox.addRow(self.tr("Barcode: "), self.product_barcode)
		formBox.addRow(self.tr("Description: "), self.product_description)
		formBox.addRow(self.tr("Quantity: "), self.product_quantity)
		formBox.addRow(self.tr("Edit Product Info? "), self.edit)
		formBox.addRow(self.tr("Submit Product Info Change? "), self.submit)
		formBox.addRow(self.tr("Delete Product? "), self.delete)
		formBox.addRow(self.ref_but)
		
		mainLayout.addWidget(self.list, 200)
		
		self.connect(self.list, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.product_info)
		self.connect(self.edit, QtCore.SIGNAL("clicked()"), self.edit_info)
		self.connect(self.submit, QtCore.SIGNAL("clicked()"), self.product_update)
		self.connect(self.ref_but, QtCore.SIGNAL("clicked()"), self.refresh)
		self.connect(self.delete, QtCore.SIGNAL("clicked()"), self.delete_product)
		
		timer = QtCore.QTimer(self)
		QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.refresh)
		timer.start(500)
		
	def product_info(self):
		item = self.list.currentItem()
		self.product_name.setReadOnly(True)
		self.product_barcode.setReadOnly(True)
		self.product_description.setReadOnly(True)
		self.product_quantity.setReadOnly(True)
		self.submit.setEnabled(False)
		self.delete.setEnabled(False)
		if (item):
			query = item.text(0)
			params = urllib.urlencode({'type_of_query': 'single_product_info', 'query': query})
		
			data = request.request(params)
		
			self.product_name.setText(str(data['name']))
			self.product_barcode.setText(str(data['barcode']))
			self.product_description.setPlainText(str(data['description']))
			self.product_quantity.setText(str(data['quantity']))
		
	def scan(self):
		query = request.receive()
		params = urllib.urlencode({'type_of_query': 'single_product_info', 'query': query})
		data = request(params, query)
		
	def edit_info(self):
		self.product_name.setReadOnly(False)
		self.product_barcode.setReadOnly(False)
		self.product_description.setReadOnly(False)
		self.product_quantity.setReadOnly(False)
		self.submit.setEnabled(True)
		self.delete.setEnabled(True)
		
	def product_update(self):
		name = self.product_name.text()
		barcode = self.product_barcode.text()
		description = self.product_description.toPlainText()
		quantity = self.product_quantity.text()
		
		params = urllib.urlencode({'type_of_query': 'update_product_info',  'name': name, 'description': description, 'query': barcode, 'quantity': quantity})
		data = request.request(params)
		
		self.refresh()
		
		item = self.list.findItems(name, QtCore.Qt.MatchExactly ,0)
		self.list.setCurrentItem(item[0])
		
		self.product_info()
		
	def delete_product(self):
		barcode = self.product_barcode.text()
		
		params = urllib.urlencode({'type_of_query': 'remove_product','query': barcode})
		data = request.request(params)
		
		self.refresh()
		
		self.product_info()
		
	def refresh(self):
		old_item = self.list.currentItem()
		if (old_item):
			query =old_item.text(0)
			
		self.list.clear()
		params = urllib.urlencode({'type_of_query': 'total_inventory'})
		data = request.request(params)
		
		for i in range(len(data)):
			item = QtGui.QTreeWidgetItem([data[i]['name'], data[i]['description'], data[i]['quantity'], data[i]['barcode'], str(data[i]['flag']) ])
			self.list.addTopLevelItem(item)
		
		if (old_item):
			item = self.list.findItems(query, QtCore.Qt.MatchExactly ,0)
			self.list.setCurrentItem(item[0])
		
			self.product_info()

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		
		self.resize(800, 600)
		self.setWindowTitle('House Inventory')
		
		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setMovable(True)
		self.setCentralWidget(self.mainTabWidget)

		self.bluetooth_tab()
		self.add_product_tab()
		self.total_inventory_tab()

		self.statusBar()
		
	def total_inventory_tab(self):
		new_inven = total_inventory(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Total Inventory")
		self.mainTabWidget.setCurrentIndex(newTab)
		
	def bluetooth_tab(self):
		new_inven = bluetooth_tab(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Bluetooth devices")
		self.mainTabWidget.setCurrentIndex(newTab)
		
	def add_product_tab(self):
		new_inven = add_product(self, self)
		newTab = self.mainTabWidget.addTab(new_inven, "Add Product")
		self.mainTabWidget.setCurrentIndex(newTab)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())