from PySide2 import QtCore, QtGui
import urllib2


class SongListModel( QtCore.QAbstractListModel ):
	def __init__( self, parent = None ):
		super( SongListModel, self ).__init__( parent )
		self.songList = []

	def rowCount( self, index=QtCore.QModelIndex() ):
		return len( self.songList )

	def data( self, index, role = QtCore.Qt.DisplayRole ):
		if not index.isValid():
			return

		item = self.songList[index.row()]
		if role == QtCore.Qt.DisplayRole:
			return item.currentItem()

	def flags( self, index ):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

	def extendList( self, list_ ):
		self.beginResetModel()
		self.songList.extend( list_ )
		self.endResetModel()

	def index( self, row, col, parent = QtCore.QModelIndex() ):
		data = self.songList[row]
		return self.createIndex( row, col, data )


class Song( object ):
	def __init__( self, id, name, image ):
		self.id = id
		self.name = name
		self.image = Image( image['url'], image['width'], image['height'] )

	def __str__( self ):
		return '%s;%s' % (self.name, self.id)

	def __repr__( self ):
		return self.__str__()


class Songs( object ):
	def __init__( self, arr ):
		self.songs = arr
		self.currentIndex = 0

	def currentItem( self ):
		return self.songs[self.currentIndex]

	def __str__( self ):
		return 'Songs %s' % (str( self.songs ))

	def __repr__( self ):
		return self.__str__()


class WebImage( QtCore.QObject ):
	def __init__( self, url, parent = None ):
		super( WebImage, self ).__init__( parent )
		self.url = urllib2.urlopen( url )
		self.byte = self.url.read()
		self._image = QtGui.QImage()
		self._image.loadFromData( self.byte )

	def qimage( self ):
		return self._image


class Image( object ):
	def __init__( self, url, width, height ):
		self.url = url
		self.width = width
		self.height = height
		self.data = None
