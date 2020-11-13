import log
import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
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
		self.deleteItemShotcut.activated.connect(self.deleteSelectedItems)
		self.deleteItemShotcut.setKey(QtGui.QKeySequence.Delete)


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
		if action == delete:
			self.deleteSelectedItems()


	def __deleteSelectedItems(self, indexes):
		res = QtWidgets.QMessageBox.question(self, 'Delete Songs', 'Are you sure that',
											 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if res == QtWidgets.QMessageBox.Yes:
			model = self.model()
			result = model.deleteRows(indexes)
			if result is False:
				Toast.error('Delete Song Item Error', 'Song is not deleted successfully')


	def deleteSelectedItems(self):
		if self.selectedIndexes():
			self.__deleteSelectedItems(self.selectedIndexes())
