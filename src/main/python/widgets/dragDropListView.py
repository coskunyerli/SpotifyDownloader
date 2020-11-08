from PySide2 import QtWidgets, QtCore


class DragDropListView(QtWidgets.QListView):
	dropped = QtCore.Signal(list)


	def __init__(self, parent = None):
		super(DragDropListView, self).__init__(parent)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)


	def dropEvent(self, event):
		try:
			urls = event.mimeData().text().split('\n')
			if urls:
				self.dropped.emit(urls)
		except Exception as e:
			print(e)



	def dragEnterEvent(self, event):
		if event.mimeData().hasHtml():
			event.acceptProposedAction()


	def dragMoveEvent(self, event):
		event.acceptProposedAction()
