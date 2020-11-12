from model.image import Image


class Song(object):
	def __init__(self, id, name, imageUrl):
		self.id = id
		self.name = name
		self.image = Image(imageUrl)


	def __str__(self):
		return f'Song({self.name}, {self.id})'


	def __repr__(self):
		return self.__str__()


class Songs(object):
	def __init__(self, arr, url):
		self.songs = arr
		self.currentIndex = 0
		self.__url = url


	def currentItem(self):
		return self.songs[self.currentIndex]


	def __str__(self):
		return 'Songs %s' % (str(self.songs))


	def __repr__(self):
		return self.__str__()


	def __eq__(self, other):
		if isinstance(other, Songs) and other.__url == self.__url:
			return True
		else:
			return False

	def getUrl(self):
		return self.__url