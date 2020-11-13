import log
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
		elif role == QtCore.Qt.UserRole:
			return item


	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled


	def extendList(self, list_):
		notInItemList = []
		for item in list_:
			if item not in self.songList:
				notInItemList.append(item)
		if notInItemList:
			self.beginResetModel()
			self.songList.extend(notInItemList)
			self.endResetModel()


	def contains(self, function):
		for item in self.songList:
			if function(item):
				return True
		return False


	def index(self, row, col = 0, parent = QtCore.QModelIndex()):
		data = self.songList[row]
		return self.createIndex(row, col, data)


	def deleteRows(self, indexes):
		if indexes:
			try:
				minIndex = min(indexes, key = lambda i: i.row())
				maxIndex = max(indexes, key = lambda i: i.row())
				self.beginRemoveRows(QtCore.QModelIndex(), minIndex.row(), maxIndex.row())
				for index in indexes:
					item = index.data(QtCore.Qt.UserRole)
					self.songList.remove(item)
				self.endRemoveRows()
				return True
			except Exception as e:
				log.error(f'Song item is not deleted successfully from model. Exception is {e}')
				return False
		else:
			return False
