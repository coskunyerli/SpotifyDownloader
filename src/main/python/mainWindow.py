import log
from PySide2 import QtGui, QtCore, QtWidgets
from mainWindowUi import Ui_MainWindow
from model.runnable.searchMusicRunnable import SearchMusicRunnable
from model.runnable.downloadMusicRunnable import DownloadMusicRunnable
from model.itemModels.songListModel import SongListModel
from widgets.dialog.progressDialog import ProgressDialog
from widgets.toast import Toast


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.key = None
		self.songsList = []
		self.outputFolder = '.'
		self.songModel = SongListModel()

		self.initWidgets()
		self.initialize()
		self.initSignalsAndSlots()


	def initWidgets(self):
		self.songList.setAcceptDrops(True)
		self.quitShortCut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
		self.quitShortCut.activated.connect(self.close)


	def initSignalsAndSlots(self):
		self.songList.dropped.connect(self.searchSongs)
		self.downloadButton.clicked.connect(self.startDownload)
		self.loadFileAction.triggered.connect(self.loadFromFile)
		self.newSongAddAction.triggered.connect(self.addNewSong)
		self.outputFolderAction.triggered.connect(self.changeOutputFolder)


	# get request from youtube and add songs to list widget

	def initialize(self):
		self.readSetting()
		self.songList.setModel(self.songModel)
		self.songList.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)


	def startDownload(self):
		progressDialog = QtWidgets.QProgressDialog(self)
		progressDialog.setWindowTitle('Download Musics')


		def downloadMusicFailed(str):
			Toast.error('Download Music Error', 'Music is not download successfully. Please try again!')
			log.error(str)


		def finishedProgress():
			progressDialog.setParent(None)
			progressDialog.close()


		def downloadSuccessful():
			progressDialog.setValue(100)
			log.info('Selected musics are downloaded successfully')


		def updateProgressBar(result):
			text, value = result
			progressDialog.setValue(value)
			progressDialog.setLabelText(text)


		if self.songModel.rowCount() > 0:
			if self.songList.selectedIndexes():
				items = list(map(lambda item: item.internalPointer(), self.songList.selectedIndexes()))
			else:
				items = self.songModel.songList

			downloadMusicRunnable = DownloadMusicRunnable(items, self.outputFolder)
			downloadMusicRunnable.failed.connect(downloadMusicFailed)
			downloadMusicRunnable.update.connect(updateProgressBar)
			downloadMusicRunnable.successful.connect(downloadSuccessful)
			downloadMusicRunnable.finished.connect(finishedProgress)
			progressDialog.canceled.connect(lambda: downloadMusicRunnable.stop())

			progressDialog.open()
			QtCore.QThreadPool.globalInstance().start(downloadMusicRunnable)
		else:
			progressDialog.close()
			progressDialog.hide()
			del progressDialog


	def changeOutputFolder(self):
		folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output Folder', self.outputFolder)
		if folder:
			self.outputFolder = folder


	def searchSongs(self, searchedSongList):
		progressDialog = ProgressDialog(self)
		progressDialog.setWindowTitle('Search Musics')


		def searchMusicSuccessful(songsList):
			if songsList.isEmpty() is False:
				self.songModel.extendList([songsList])
				log.info(f'Search is done successfully. {searchedSongList}')
			else:
				Toast.warning('Invalid Song', 'Searched song is not valid song.')
				log.warning(f'Searched song is not valid song.Song url is {songsList.getUrl()}')


		def searchMusicFailed(str):
			Toast.error('Search Music Error', 'Music is not searched successfully')
			log.error(str)


		def searchMusicUpdate(result):
			name, value = result
			progressDialog.setValue(value)
			progressDialog.setLabelText(name)


		def searchMusicFinished():
			progressDialog.setParent(None)
			progressDialog.close()


		if searchedSongList:
			searchMusicRunnable = SearchMusicRunnable(searchedSongList)
			searchMusicRunnable.successful.connect(searchMusicSuccessful)
			searchMusicRunnable.failed.connect(searchMusicFailed)
			searchMusicRunnable.finished.connect(searchMusicFinished)
			searchMusicRunnable.update.connect(searchMusicUpdate)
			progressDialog.canceled.connect(lambda: searchMusicRunnable.stop())
			progressDialog.open()

			QtCore.QThreadPool.globalInstance().start(searchMusicRunnable)


	def loadFromFile(self):
		filename, result = QtWidgets.QFileDialog.getOpenFileName(self, 'Select File to Load Songs', '../../../',
																 'Song File (*.txt)')
		if result and filename:
			file_ = open(filename)
			try:
				text = file_.read()
				songList = text.split('\n')
				self.searchSongs(songList)
				file_.close()
			except Exception as e:
				log.error(f'Song file is not loaded successfully. Exception is {e}')
				Toast.error('Song File Loading Error', 'Song file is not loaded successfully')
				file_.close()


	def addNewSong(self):
		text, res = QtWidgets.QInputDialog.getText(self, 'Search Song', 'Enter a title for song',
												   QtWidgets.QLineEdit.Normal)
		if text and res:
			try:
				self.searchSongs([text])
			except Exception as e:
				log.error(f'Song is not added successfully. Exception is {e}')
				Toast.error('Song Add Error', 'Song is not added successfully')


	def closeEvent(self, event):
		self.saveSetting()
		super(MainWindow, self).closeEvent(event)


	def readSetting(self):
		try:
			setting = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "SpotifyDownloader",
									   "settings")
			self.outputFolder = setting.value('output', '.')
			size = setting.value('size', QtCore.QSize(600, 400))
			self.resize(size)
		except Exception as e:
			log.warning(f'Read setting is not executed successfully. Exception is {e}')


	def saveSetting(self):
		try:
			setting = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "SpotifyDownloader",
									   "settings")
			if self.key is not None:
				setting.setValue('key', self.key)
			setting.setValue('output', self.outputFolder)
			setting.setValue('size', self.size())
		except Exception as e:
			log.warning(f'Save setting is not executed successfully. Exception is {e}')
