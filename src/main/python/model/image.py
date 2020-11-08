import PySide2.QtGui as QtGui
from urllib.request import urlopen


class Image(object):
	def __init__(self, url):
		self.url = url
		if url:
			byte = urlopen(url).read()
			image = QtGui.QImage()
			image.loadFromData(byte)
			if image:
				self.data = image
			else:
				self.data = QtGui.QImage()
		else:
			self.data = QtGui.QImage()
