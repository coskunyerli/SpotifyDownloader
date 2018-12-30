from __future__ import unicode_literals

import json
import urllib
import urllib2

from PySide2 import QtGui, QtCore, QtWidgets
from mainWindowUi import Ui_MainWindow
import os
import youtube_dl

from models import SongListModel, Song, Songs
from threads import Thread


class MainWindow( Ui_MainWindow, QtWidgets.QMainWindow ):
	def __init__( self, parent = None ):
		super( MainWindow, self ).__init__( parent )
		self.setupUi( self )
		self._thread = Thread( self.downloadSongs )
		self._thread.update.connect( self.updateDialog )
		self.dialog = QtWidgets.QProgressDialog( parent )
		self.dialog.close()
		self.key = None
		self.songsList = []  # , 'Wonderwall - Oasis', 'You Give Love A Bad Name - Bon Jovi'
		self.outputFolder = '.'

		self.songModel = SongListModel()

		self.initWidgets()
		self.initialize()
		self.initSignalsAndSlots()

	def initWidgets( self ):
		self.songList.setAcceptDrops( True )
		self.quitShortCut = QtWidgets.QShortcut( QtGui.QKeySequence( QtCore.Qt.Key_Escape ), self )
		self.quitShortCut.activated.connect( self.close )

	def initSignalsAndSlots( self ):
		self.songList.dropped.connect( self.droppedSongs )
		self.downloadButton.clicked.connect( self.startDownload )
		self._thread.successful.connect( self.downloadSuccessful )
		self.changeTokenAction.triggered.connect( self.changeToken )
		self.loadFileAction.triggered.connect( self.loadFromFile )
		self.outputFolderAction.triggered.connect( self.changeOutputFolder )

	# get request from youtube and add songs to list widget

	def initialize( self ):
		self.readSetting()
		self.songList.setModel( self.songModel )

		size = QtCore.QSize( 600, 400 )
		self.setFixedSize( size )
		self.songList.setAttribute( QtCore.Qt.WA_MacShowFocusRect, 0 )

	def search( self, title, key ):
		f = { 'part': 'snippet', 'maxResult': 1, 'q': title, 'key': key }
		encode = urllib.urlencode( f )
		url = "https://www.googleapis.com/youtube/v3/search/?%s" % (encode)
		try:
			request = urllib2.urlopen( url ).read()
			requestJson = json.loads( request )
			items = requestJson.get( 'items' )
			if items:
				return items
			else:
				print 'Items is empty in url %s' % url
				return None
		except:
			print 'Error while get item from url %s' % url
			return None

	def searchSong( self ):
		arr = self.searchList( self.songsList, self.key )
		arr = map( lambda items: Songs( map( lambda item: Song( item['id']['videoId'], item['snippet']['title'],
																item['snippet']['thumbnails']['default'] ), items ) ),
				   arr )
		self.songModel.extendList( arr )

	def searchList( self, songList, key ):
		arr = []
		for title in songList:
			items = self.search( title, key )
			if items is not None:
				arr.append( items )
		return arr

	def startDownload( self ):
		if self.songModel.rowCount() > 0:
			if self.songList.selectedIndexes():
				items = map( lambda item: item.internalPointer(), self.songList.selectedIndexes() )
			else:
				items = self.songModel.songList
			self.dialog.open()
			self._thread.start( songsIndices = items )

	def downloadSongs( self, updateSignal, songsIndices ):
		path = os.path.join( self.outputFolder, '%(title)s.%(ext)s)' )
		download_options = {
			'format': 'bestaudio/best',
			'outtmpl': path,
			'nocheckcertificate': True,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		lenght = len( songsIndices )
		step = 100.0 / lenght
		with youtube_dl.YoutubeDL( download_options ) as dl:
			for i in range( lenght ):
				songs = songsIndices[i]
				song = songs.currentItem()
				updateSignal.emit( ( song.name, i * step) )
				dl.download( ['https://www.youtube.com/watch?v=%s' % song.id] )

		return True

	def updateDialog( self, obj ):
		self.dialog.setLabelText( obj[0] )
		self.dialog.setValue( obj[1] )

	def downloadSuccessful( self, result ):
		self.dialog.setValue( 100 )
		self.dialog.close()

	# download songs to the current folder

	def changeToken( self ):
		text, result = QtWidgets.QInputDialog.getText( self, 'Token', 'Get Token' )
		if result and text:
			self.key = text
			self.tokenLabel.setText( self.key )

	def changeOutputFolder( self ):
		folder = QtWidgets.QFileDialog.getExistingDirectory( self, 'Output Folder', self.outputFolder )
		if folder:
			self.outputFolder = folder

	def droppedSongs( self, songList ):
		if songList:
			self.songsList = songList
			self.searchSong()

	def loadFromFile( self ):
		filename, result = QtWidgets.QFileDialog.getOpenFileName( self, 'Select File to Load Songs', './',
																  'Song File (*.txt)' )
		if result and filename:
			file_ = open( filename )
			try:
				text = file_.read()
				songList = text.split( '\n' )
				self.droppedSongs( songList )
				file_.close()
			except:
				file_.close()

	def closeEvent( self, event ):
		self.saveSetting()
		super( MainWindow, self ).closeEvent( event )

	def readSetting( self ):
		setting = QtCore.QSettings( 'settings.ini', QtCore.QSettings.NativeFormat )
		value = setting.value( 'key' )
		if value:
			self.key = value
			self.tokenLabel.setText( 'Token : %s' % self.key )
		else:
			self.changeToken()
			if self.key is None:
				QtWidgets.QMessageBox.information( self, 'Token Info',
												   'Token is not initialized, so request is limited' )

		self.outputFolder = setting.value( 'output', '.' )

	def saveSetting( self ):
		setting = QtCore.QSettings( 'settings.ini', QtCore.QSettings.NativeFormat )
		if self.key is not None:
			setting.setValue( 'key', self.key )
		setting.setValue( 'output', self.outputFolder )
