import json

import PySide2.QtCore as QtCore
import requests
import static
from model.runnable.baseRunnable import BaseRunnable
from model.song import Song, Songs
from model.stopThreadSignal import StopThreadSignal
from youtube_search import YoutubeSearch


class SearchMusicRunnable(QtCore.QObject, BaseRunnable):
	successful = QtCore.Signal(Songs)
	failed = QtCore.Signal(str)
	finished = QtCore.Signal()
	update = QtCore.Signal(object)


	def __init__(self, urls):
		QtCore.QObject.__init__(self)
		BaseRunnable.__init__(self)
		self.__stopSignal = StopThreadSignal()
		self.__urls = urls
		self.timeout = 30


	def run(self):
		lenght = len(self.__urls)
		step = 100.0 / lenght
		try:
			for i in range(len(self.__urls)):

				url = self.__urls[i]
				if static.is_url(url):
					songInDict = self.getSongListInDict(url)
					if songInDict is not None:
						songName = self.getSongNameAndArtistInString(songInDict)
						if songName is not None:
							self.update.emit((songName, i * step))
							items = self.searchSongs(songName)
							if items:
								songsList = Songs(list(map(lambda item: self.__createSong(item), items)), url)
								if self.__stopSignal.isStopped():
									return

								self.successful.emit(songsList)
						else:
							self.failed.emit(f'Search music is failed. Exception is song name is invalid {songInDict}')
					else:
						self.failed.emit(f'Search music is failed. Exception is url is invalid {url}')
				else:
					songName = url
					self.update.emit((songName, i * step))
					items = self.searchSongs(songName)
					if items:
						songsList = Songs(list(map(lambda item: self.__createSong(item), items)), url)
						if self.__stopSignal.isStopped():
							return
						self.successful.emit(songsList)
		except Exception as e:
			self.failed.emit(f'Search music is failed. Exception is {str(e)}')
		finally:
			self.finished.emit()


	def search(self, title):
		results = YoutubeSearch(title, max_results = 5, timeout = self.timeout).to_json()
		resultsInDict = json.loads(results)
		return resultsInDict.get('videos', [])


	def searchSongs(self, title):
		items = self.search(title)
		return items


	def __createSong(self, songInDict):
		if songInDict.get('thumbnails') and len(songInDict.get('thumbnails')) > 0:
			imageUrl = songInDict['thumbnails'][0]
		else:
			imageUrl = ''

		return Song(songInDict['id'], songInDict['title'], imageUrl, songInDict['duration'])


	def getSongListInDict(self, url):
		spotifyInfo = None
		htmlContent = requests.get(url, timeout = self.timeout)
		if htmlContent.status_code == 200:
			html = htmlContent.text
			startTagText = 'Spotify.Entity = '
			endTagText = '</script>'
			if startTagText in html:
				startIndex = html.index(startTagText) + len(startTagText)
				html = html[startIndex:]
				if endTagText in html:
					endIndex = html.index(endTagText)
					html = html[:endIndex]
					index = html.rfind(';')
					if index != -1:
						html = html[:index]
						spotifyInfo = json.loads(html)
		return spotifyInfo


	def getSongNameAndArtistInString(self, spotifyInfo):
		songName = spotifyInfo.get('name')
		artists = spotifyInfo.get('artists', [])
		try:
			artistsInString = ' '.join(map(lambda artist: artist['name'], artists))
			return f'{songName} - {artistsInString}'
		except Exception as e:
			return None


	def stop(self):
		self.__stopSignal.stop(True)
