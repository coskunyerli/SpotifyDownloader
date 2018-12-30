# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created: Sat Dec 22 22:46:11 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
import os

from PySide2 import QtCore, QtGui, QtWidgets, QtXml

from models import WebImage


class Ui_MainWindow( object ):
	def setupUi( self, MainWindow ):
		MainWindow.setObjectName( "MainWindow" )
		self.centralwidget = QtWidgets.QWidget( MainWindow )
		self.centralwidget.setObjectName( "centralwidget" )
		self.verticalLayout = QtWidgets.QVBoxLayout( self.centralwidget )
		self.verticalLayout.setObjectName( "verticalLayout" )
		self.songList = DragDropListView( self.centralwidget )

		delegate1 = SongItemDelegate( self.songList )
		self.songList.setItemDelegate( delegate1 )
		self.songList.setSelectionMode( QtWidgets.QAbstractItemView.ExtendedSelection )

		self.songList.setObjectName( "songList" )
		self.songList.setStyleSheet( 'background-color:"#323232"' )
		self.verticalLayout.addWidget( self.songList )
		self.verticalLayout.setContentsMargins( 0, 0, 0, 0 )
		MainWindow.setCentralWidget( self.centralwidget )
		self.menubar = MainWindow.menuBar()
		menu = QtWidgets.QMenu( 'File' )
		self.menubar.addMenu( menu )
		self.loadFileAction = QtWidgets.QAction( MainWindow )
		self.loadFileAction.setText( 'Load Song From File' )
		self.loadFileAction.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_O ) )
		menu.addAction( self.loadFileAction )
		self.changeTokenAction = QtWidgets.QAction( MainWindow )
		self.changeTokenAction.setText( 'Change Token' )
		self.changeTokenAction.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_T ) )
		menu.addAction( self.changeTokenAction )
		self.outputFolderAction = QtWidgets.QAction( MainWindow )
		self.outputFolderAction.setText( 'Change Output Folder' )
		menu.addAction( self.outputFolderAction )
		self.menubar.setObjectName( "menubar" )
		MainWindow.setMenuBar( self.menubar )
		# self.statusbar = QtWidgets.QStatusBar( MainWindow )
		# self.statusbar.setObjectName( "statusbar" )
		# MainWindow.setStatusBar( self.statusbar )
		self.downloadButton = QtWidgets.QPushButton( MainWindow )
		self.verticalLayout.addWidget( self.downloadButton )

		self.tokenLabel = QtWidgets.QLabel( MainWindow )
		self.tokenLabel.setText( '' )
		self.tokenLabel.setAlignment( QtCore.Qt.AlignBottom )
		spacer = QtWidgets.QSpacerItem( 0, 12 )
		self.verticalLayout.addItem( spacer )
		self.verticalLayout.addWidget( self.tokenLabel )
		spacer = QtWidgets.QSpacerItem( 0, 8 )
		self.verticalLayout.addItem( spacer )
		self.verticalLayout.setSpacing( 0 )

		self.retranslateUi( MainWindow )
		QtCore.QMetaObject.connectSlotsByName( MainWindow )

	def retranslateUi( self, MainWindow ):
		MainWindow.setWindowTitle( "Spotify Downloader" )
		self.downloadButton.setText( 'Download' )


class DragDropListView( QtWidgets.QListView ):
	dropped = QtCore.Signal( list )

	def __init__( self, parent = None ):
		super( DragDropListView, self ).__init__( parent )
		self.setAcceptDrops( True )
		self.setDragEnabled( True )
		self.setDragDropMode( QtWidgets.QAbstractItemView.DragDrop )
		self.dragLabel = DragLabel( self )
		self.dragLabel.setGeometry( self.geometry() )
		self.dragLabel.setAlignment( QtCore.Qt.AlignCenter )
		pixmap = QtGui.QPixmap( os.path.join( 'images', 'drag_drop.png' ) )
		self.dragLabel.setPixmap( pixmap )

	def resizeEvent( self, event ):
		super( DragDropListView, self ).resizeEvent( event )
		self.dragLabel.setGeometry( self.geometry() )

	def dropEvent( self, event ):
		dom = QtXml.QDomDocument()
		html = event.mimeData().html()
		dom.setContent( html )
		arr = []
		list_ = dom.elementsByTagName( 'a' )
		for i in range( list_.count() ):
			arr.append( list_.at( i ).toElement().text() )

		if arr:
			self.dragLabel.hide()
		self.dropped.emit( arr )

	def dragEnterEvent( self, event ):
		if event.mimeData().hasHtml():
			event.acceptProposedAction()

	def dragMoveEvent( self, event ):
		event.acceptProposedAction()


class DragLabel( QtWidgets.QLabel ):
	def __init__( self, parent = None ):
		super( DragLabel, self ).__init__( parent )
		self.setAcceptDrops( True )

	def dragEnterEvent( self, event ):
		self.parent().dragEnterEvent( event )

	def dropEvent( self, event ):
		self.parent().dropEvent( event )


class SongItemDelegate( QtWidgets.QItemDelegate ):
	def __init__( self, parent = None ):
		super( SongItemDelegate, self ).__init__( parent )

	def paint( self, painter, option, index ):
		song = index.internalPointer()
		data = song.currentItem()
		painter.setRenderHint( QtGui.QPainter.Antialiasing, True )
		rect = option.rect
		# print rect
		if option.state & QtWidgets.QStyle.State_Selected:
			painter.fillRect( rect, QtGui.QBrush( QtGui.QColor( '#4A4A4A' ) ) )
		if data.image.data is None:
			image = WebImage( data.image.url )
			data.image.data = image.qimage()
		imageRect = QtCore.QRect( rect.left(), rect.top(), data.image.width, data.image.height )
		painter.drawImage( imageRect, data.image.data, data.image.data.rect() )
		textRect = rect.adjusted( imageRect.width() + 4, 0, 0, 0 )
		painter.drawText( textRect, QtCore.Qt.AlignVCenter, data.name )
		lineRect = QtCore.QRect( imageRect.topLeft(), QtCore.QSize( rect.width(), 2 ) )
		painter.fillRect( lineRect, QtGui.QColor( '#202020' ) )

	def sizeHint( self, option, index ):
		size = super( SongItemDelegate, self ).sizeHint( option, index )
		song = index.internalPointer()
		item = song.currentItem()
		size.setHeight( item.image.height )
		return size

	def createEditor( self, parent, option, index ):
		comboBox = QtWidgets.QComboBox( parent )
		song = index.internalPointer()
		comboBox.addItems( map( lambda item: item.name, song.songs ) )
		return comboBox

	def setEditorData( self, comboBox, index ):
		song = index.internalPointer()
		comboBox.setCurrentIndex( song.currentIndex )

	def updateEditorGeometry( self, comboBox, option, index ):
		song = index.internalPointer()
		data = song.currentItem()
		rect = option.rect
		imageRect = QtCore.QRect( rect.left(), rect.top(), data.image.width, data.image.height )
		rect.adjust( imageRect.width(), 0, 0, 0 )
		comboBox.setGeometry( rect )

	def setModelData( self, comboBox, model, index ):
		song = index.internalPointer()
		song.currentIndex = comboBox.currentIndex()
