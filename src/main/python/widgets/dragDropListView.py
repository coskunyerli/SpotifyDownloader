import log
import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
import static
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
		self.label = QtWidgets.QLabel(self)
		self.label.setText('DROP SPOTIFY ITEMS HERE')
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setStyleSheet('font-size:40pt;color:#444444')
		self.label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)


	def initShortcuts(self):
		self.deleteItemShotcut = QtWidgets.QShortcut(self)
		self.deleteItemShotcut.activated.connect(self.deleteSelectedItems)
		self.deleteItemShotcut.setKey(QtGui.QKeySequence.Delete)


	def setModel(self, model: QtCore.QAbstractItemModel):
		super(DragDropListView, self).setModel(model)
		model.rowsInserted.connect(self.__itemSizeChanged)
		model.rowsInserted.connect(self.__itemSizeChanged)
		model.rowsRemoved.connect(self.__itemSizeChanged)
		model.modelReset.connect(self.__itemSizeChanged)


	def __itemSizeChanged(self):
		if self.model() is not None and self.model().rowCount() > 0:
			self.label.hide()
		else:
			self.label.show()


	def resizeEvent(self, event):
		super(DragDropListView, self).resizeEvent(event)
		self.label.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), event.size()))


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
		if event.mimeData().hasText():
			urls = event.mimeData().text().split('\n')
			for url in urls:
				if static.is_url(url) is False:
					return
			event.acceptProposedAction()


	def dragMoveEvent(self, event):
		event.acceptProposedAction()


	def __showContextMenu(self, point):
		globalPos = self.mapToGlobal(point)
		contextMenu = QtWidgets.QMenu()
		if self.selectedIndexes():
			if len(self.selectedIndexes()) == 1:
				edit = contextMenu.addAction('Edit')
			else:
				edit = None
			delete = contextMenu.addAction('Remove')

			action = contextMenu.exec_(globalPos)
			if action == delete:
				self.deleteSelectedItems()
			elif action == edit:
				self.edit(self.currentIndex())


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
