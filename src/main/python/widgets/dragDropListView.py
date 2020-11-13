import log
from PySide2 import QtWidgets, QtCore
from widgets.toast import Toast


class DragDropListView(QtWidgets.QListView):
	dropped = QtCore.Signal(list)


	def __init__(self, parent = None):
		super(DragDropListView, self).__init__(parent)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.__showContextMenu)

		self.initShortcuts()


	def initShortcuts(self):
		self.deleteItemShotcut = QtWidgets.QShortcut(self)
		self.deleteItemShotcut.activated.connect(self.__deleteSelectedItems)


	def dropEvent(self, event):
		try:
			urls = event.mimeData().text().split('\n')
			model = self.model()
			if model is not None:
				notContainsUrl = list(
					filter(lambda url: model.contains(lambda songs: songs.getUrl() == url) is False, urls))
				if notContainsUrl:
					self.dropped.emit(notContainsUrl)
		except Exception as e:
			log.error(f'Drop event has error in drag drop list view. Exception is {e}')


	def dragEnterEvent(self, event):
		if event.mimeData().hasHtml():
			event.acceptProposedAction()


	def dragMoveEvent(self, event):
		event.acceptProposedAction()


	def __showContextMenu(self, point):
		globalPos = self.mapToGlobal(point)
		contextMenu = QtWidgets.QMenu()
		delete = contextMenu.addAction('Remove')

		action = contextMenu.exec_(globalPos)
		if self.selectedIndexes():
			if action == delete:
				self.__deleteSelectedItems(self.selectedIndexes())


	def __deleteSelectedItems(self, indexes):
		res = QtWidgets.QMessageBox.question(self, 'Delete Songs', 'Are you sure that',
											 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if res == QtWidgets.QMessageBox.Yes:
			model = self.model()
			result = model.deleteRows(indexes)
			if result is False:
				Toast.error('Delete Song Item Error', 'Song is not deleted successfully')
