from PySide2 import QtCore


class SongListModel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		super(SongListModel, self).__init__(parent)
		self.songList = []


	def rowCount(self, index = QtCore.QModelIndex()):
		return len(self.songList)


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if not index.isValid():
			return

		item = self.songList[index.row()]
		if role == QtCore.Qt.DisplayRole:
			return item.currentItem()


	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled


	def extendList(self, list_):
		self.beginResetModel()
		self.songList.extend(list_)
		self.endResetModel()


	def index(self, row, col = 0, parent = QtCore.QModelIndex()):
		data = self.songList[row]
		return self.createIndex(row, col, data)