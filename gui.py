#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui

debug = 0
version = ".01 alpha"

class total_inventory(QtGui.QWidget):
	def __init__(self, parent, main):
		QtGui.QWidget.__init__(self)
		

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.mainTabWidget = QtGui.QTabWidget(self)
		self.mainTabWidget.setTabsClosable(True)
		self.mainTabWidget.setMovable(True)
		self.setCentralWidget(self.mainTabWidget)

		self.total_inventory_tab

		self.statusBar()