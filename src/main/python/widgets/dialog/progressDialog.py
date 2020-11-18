import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore


class ProgressDialog(QtWidgets.QDialog):
	canceled = QtCore.Signal()


	def __init__(self, parent = None):
		super(ProgressDialog, self).__init__(parent)
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(8, 16, 8, 0)
		self.labelText = QtWidgets.QLabel(self)
		self.labelText.setAlignment(QtCore.Qt.AlignCenter)
		self.progressBar = QtWidgets.QProgressBar(self)
		self.progressBar.setFixedHeight(6)
		self.progressBar.setTextVisible(False)
		self.buttonWidget = QtWidgets.QWidget(self)
		self.buttonWidgetLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
		self.buttonWidgetLayout.addItem(
			QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.cancelButton = QtWidgets.QPushButton(self.buttonWidget)
		self.cancelButton.setText('Cancel')
		self.buttonWidgetLayout.addWidget(self.cancelButton)

		self.verticalLayout.addWidget(self.labelText)
		self.verticalLayout.addWidget(self.progressBar)
		self.verticalLayout.addWidget(self.buttonWidget)

		self.cancelButton.clicked.connect(self.__clickCancelButton)


	def __clickCancelButton(self):
		self.canceled.emit()


	def setLabelText(self, text):
		self.labelText.setText(text)


	def setValue(self, value):
		self.progressBar.setValue(value)
