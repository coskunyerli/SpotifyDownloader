import json
import PySide2.QtCore as QtCore
import static
from model.contentFetcher import YoutubeFetcher, SpotifyFetcher
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
		try:
			i = 0
			for url in self.__urls:
				if static.is_url(url):
					songNameList = self.getSongNameList(url)
					if songNameList is not None:
						for songName, songUrl in songNameList:
							self.update.emit((songName, i * 100.0 / (lenght + len(songNameList))))
							items = self.searchSongs(songName)
							if items:
								songList = map(lambda item: self.__createSong(item), items)
								songsList = Songs(list(filter(lambda song: isinstance(song, Song), songList)), songUrl)
								if self.__stopSignal.isStopped():
									return
								self.successful.emit(songsList)
							i += 1
					else:
						self.failed.emit(f'Search music is failed. Exception is song name is invalid {url}')
				else:
					songName = url
					self.update.emit((songName, i * 100.0 / lenght))
					items = self.searchSongs(songName)
					if items:
						songsList = Songs(list(map(lambda item: self.__createSong(item), items)), url)
						if self.__stopSignal.isStopped():
							return
						self.successful.emit(songsList)
					i += 1
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
		if 'id' in songInDict and 'title' in songInDict and 'duration' in songInDict and songInDict['duration'] != 0:
			return Song(songInDict['id'], songInDict['title'], imageUrl, songInDict['duration'])
		else:
			return None


	def getSongNameList(self, url):
		fetcher = self.getContentFetcher(url)
		if fetcher is not None:
			return fetcher.fetchContent()
		else:
			return None


	def stop(self):
		self.__stopSignal.stop(True)


	def getContentFetcher(self, url):
		if 'www.youtube.com' in url:
			return YoutubeFetcher(url, self.timeout)
		elif 'open.spotify.com' in url:
			return SpotifyFetcher(url, self.timeout)
		else:
			return None
