from PySide2 import QtGui, QtCore, QtWidgets
from mainWindowUi import Ui_MainWindow
from model.runnable.searchMusicRunnable import SearchMusicRunnable
from model.runnable.downloadMusicRunnable import DownloadMusicRunnable
from model.itemModels.songListModel import SongListModel


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.key = None
		self.songsList = []  # , 'Wonderwall - Oasis', 'You Give Love A Bad Name - Bon Jovi'
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
			print(str)


		def finishedProgress():
			progressDialog.setParent(None)
			progressDialog.close()


		def downloadSuccessful():
			progressDialog.setValue(100)


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


	def changeOutputFolder(self):
		folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output Folder', self.outputFolder)
		if folder:
			self.outputFolder = folder


	def searchSongs(self, searchedSongList):
		progressDialog = QtWidgets.QProgressDialog(self)
		progressDialog.setWindowTitle('Search Musics')


		def searchMusicSuccessful(songsList):
			self.songModel.extendList([songsList])


		def searchMusicFailed(str):
			print(str)


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
			except:
				file_.close()


	def closeEvent(self, event):
		self.saveSetting()
		super(MainWindow, self).closeEvent(event)


	def readSetting(self):
		setting = QtCore.QSettings('settings.ini', QtCore.QSettings.NativeFormat)
		self.outputFolder = setting.value('output', '.')
		size = setting.value('size', QtCore.QSize(600, 400))
		self.resize(size)


	def saveSetting(self):
		setting = QtCore.QSettings('settings.ini', QtCore.QSettings.NativeFormat)
		if self.key is not None:
			setting.setValue('key', self.key)
		setting.setValue('output', self.outputFolder)
		setting.setValue('size', self.size())