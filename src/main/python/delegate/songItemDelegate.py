from PySide2 import QtWidgets, QtCore, QtGui


class SongItemDelegate(QtWidgets.QItemDelegate):
	def __init__(self, parent = None):
		super(SongItemDelegate, self).__init__(parent)
		self.__imageSize = QtCore.QSize(160, 90)


	def paint(self, painter, option, index):
		song = index.internalPointer()
		currentSong = song.currentItem()
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		rect = option.rect
		# print rect
		if option.state & QtWidgets.QStyle.State_Selected:
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#4A4A4A')))

		imageRect = QtCore.QRect(rect.left(), rect.top(), self.__imageSize.width(), self.__imageSize.height())
		painter.drawImage(imageRect, currentSong.image.data, currentSong.image.data.rect())
		textRect = rect.adjusted(imageRect.width() + 4, 0, 0, 0)
		painter.drawText(textRect, QtCore.Qt.AlignVCenter, currentSong.name)
		lineRect = QtCore.QRect(imageRect.topLeft(), QtCore.QSize(rect.width(), 2))
		painter.fillRect(lineRect, QtGui.QColor('#202020'))


	def sizeHint(self, option, index):
		size = super(SongItemDelegate, self).sizeHint(option, index)
		size.setHeight(self.__imageSize.height())
		return size


	def createEditor(self, parent, option, index):
		comboBox = QtWidgets.QComboBox(parent)
		song = index.internalPointer()
		comboBox.addItems(list(map(lambda item: item.name, song.songs)))
		return comboBox


	def setEditorData(self, comboBox, index):
		song = index.internalPointer()
		comboBox.setCurrentIndex(song.currentIndex)


	def updateEditorGeometry(self, comboBox, option, index):
		rect = option.rect
		imageRect = QtCore.QRect(rect.left(), rect.top(), self.__imageSize.width(), self.__imageSize.height())
		rect.adjust(imageRect.width(), 0, 0, 0)
		comboBox.setGeometry(rect)


	def setModelData(self, comboBox, model, index):
		song = index.internalPointer()
		song.currentIndex = comboBox.currentIndex()
