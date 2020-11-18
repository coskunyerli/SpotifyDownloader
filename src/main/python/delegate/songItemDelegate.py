from PySide2 import QtWidgets, QtCore, QtGui


class SongItemDelegate(QtWidgets.QStyledItemDelegate):
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
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#454545')))
		else:
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#303030')))

		imageRect = QtCore.QRect(rect.left(), rect.top(), self.__imageSize.width(), self.__imageSize.height())
		painter.drawImage(imageRect, currentSong.image.data, currentSong.image.data.rect())
		painter.save()
		painter.setPen(QtGui.QColor('#dddddd'))
		textRect = rect.adjusted(imageRect.width() + 16, 0, 0, 0)
		painter.drawText(textRect, QtCore.Qt.AlignVCenter, currentSong.name)

		durationWidth = painter.fontMetrics().width(song.currentItem().duration)
		durationRect = QtCore.QRect(rect.right() - (durationWidth + 8), rect.top(), durationWidth, rect.height())
		painter.drawText(durationRect, QtCore.Qt.AlignVCenter, song.currentItem().duration)

		lineRect = QtCore.QRect(imageRect.topLeft(), QtCore.QSize(rect.width(), 2))
		painter.restore()

		painter.fillRect(lineRect, QtGui.QColor('#202020'))


	def sizeHint(self, option, index):
		size = super(SongItemDelegate, self).sizeHint(option, index)
		size.setHeight(self.__imageSize.height())
		return size


	def createEditor(self, parent, option, index):
		comboBox = QtWidgets.QComboBox(parent)
		song = index.internalPointer()
		comboBox.addItems(list(map(lambda item: f'{item.name}    {item.duration}', song.songs)))
		return comboBox


	def setEditorData(self, comboBox, index):
		song = index.internalPointer()
		comboBox.setCurrentIndex(song.currentIndex)


	def updateEditorGeometry(self, comboBox, option, index):
		rect = option.rect
		imageRect = QtCore.QRect(rect.left(), rect.top(), self.__imageSize.width(), self.__imageSize.height())
		rect.adjust(imageRect.width(), 0, 0, 0)
		comboBox.setGeometry(rect)
		comboBox.showPopup()


	def setModelData(self, comboBox, model, index):
		song = index.internalPointer()
		song.currentIndex = comboBox.currentIndex()
