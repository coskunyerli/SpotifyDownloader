# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created: Sat Dec 22 22:46:11 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from delegate.songItemDelegate import SongItemDelegate
from widgets.dragDropListView import DragDropListView


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		self.centralwidget = QtWidgets.QFrame(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName("verticalLayout")
		self.songList = DragDropListView(self.centralwidget)
		self.songList.setStyleSheet('background-color:#202020')

		delegate1 = SongItemDelegate(self.songList)
		self.songList.setItemDelegate(delegate1)
		self.songList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

		self.songList.setObjectName("songList")
		self.verticalLayout.addWidget(self.songList)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = MainWindow.menuBar()
		menu = QtWidgets.QMenu('File')
		self.menubar.addMenu(menu)
		self.loadFileAction = QtWidgets.QAction(MainWindow)
		self.loadFileAction.setText('Load Song From File')
		self.loadFileAction.setShortcut(QtGui.QKeySequence('CTRL+O'))
		menu.addAction(self.loadFileAction)

		self.newSongAddAction = QtWidgets.QAction(MainWindow)
		self.newSongAddAction.setText('Add New Song')
		self.newSongAddAction.setShortcut(QtGui.QKeySequence('CTRL+N'))
		menu.addAction(self.newSongAddAction)

		self.outputFolderAction = QtWidgets.QAction(MainWindow)
		self.outputFolderAction.setText('Change Output Folder')
		# self.outputFolderAction.setShortcut(QtGui.QKeySequence('CTRL+C'))
		menu.addAction(self.outputFolderAction)
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)

		self.downloadButton = QtWidgets.QPushButton(MainWindow)
		self.downloadButton.setObjectName('downloadButton')
		self.verticalLayout.addWidget(self.downloadButton)

		size = QtCore.QSize(600, 400)
		MainWindow.setMinimumSize(size)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle("Spotify Downloader")
		self.downloadButton.setText('Download')
