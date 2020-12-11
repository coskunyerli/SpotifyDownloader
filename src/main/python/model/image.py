import PySide2.QtGui as QtGui
from urllib.request import urlopen
import ssl
import log


class Image(object):
	def __init__(self, url):
		self.url = url
		if url:
			try:
				gcontext = ssl.SSLContext()
				byte = urlopen(url, context = gcontext).read()
				image = QtGui.QImage()
				image.loadFromData(byte)
				if image:
					self.data = image
				else:
					self.data = QtGui.QImage()
			except Exception as e:
				log.error(f'Image of song is not loaded successfully. Exception is {e}')
		else:
			self.data = QtGui.QImage()
