import json

import log
import requests


class BaseFetcher(object):
	def fetchContent(self):
		pass


class YoutubeFetcher(BaseFetcher):
	def __init__(self, url, timeout):
		super(YoutubeFetcher, self).__init__()
		self.url = url
		self.timeout = timeout


	def fetchContent(self):
		htmlContent = requests.get(self.url, timeout = self.timeout)
		if htmlContent.status_code == 200:
			try:
				html = htmlContent.text
				searchText = '<meta name="title'
				if searchText in html:
					startIndex = html.index(searchText)
					html = html[startIndex:]
					endText = '>'
					if endText in html:
						endIndex = html.index(endText)
						metaData = html[0:endIndex]
						contentStartText = 'content="'

						if contentStartText in metaData:
							contentStartIndex = metaData.index(contentStartText)
							metaData = metaData[contentStartIndex + len(contentStartText):]
							if '"' in metaData:
								contentEndIndex = metaData.index('"')
								metaData = metaData[:contentEndIndex]
								if metaData and metaData != 'null':
									return [(metaData, self.url)]
			except Exception as e:
				log.error(f'Invalid fetched content for youtube. Exception is {e}')
				return None
			log.warning(f'Invalid fetched content for youtube. url is {self.url}')
			return None


class SpotifyFetcher(BaseFetcher):
	class UrlType:
		TRACK = 0
		PLAYLIST = 1
		ALBUM = 2


	def __init__(self, url, timeout):
		super(SpotifyFetcher, self).__init__()
		self.url = url
		self.timeout = timeout


	def fetchContent(self):
		urlType = self.getUrlType()
		if urlType == SpotifyFetcher.UrlType.TRACK:
			songInDict = self.getSongListInDict()
			if songInDict is not None and 'uri' in songInDict:
				return [(self.getSongNameAndArtistInString(songInDict), songInDict['uri'])]
			else:
				return None
		elif urlType == SpotifyFetcher.UrlType.PLAYLIST:
			songInDict = self.getSongListInDict()
			if songInDict is not None:
				songNameList = self.getSongFromList(songInDict)
				return songNameList
			else:
				return None
		elif urlType == SpotifyFetcher.UrlType.ALBUM:
			songInDict = self.getSongListInDict()
			if songInDict is not None:
				songNameList = self.getSongFromAlbum(songInDict)
				return songNameList
			else:
				return None
		else:
			log.warning(f'Invalid spotify url type. Url is {self.url}')
			return None


	def getSongListInDict(self):
		spotifyInfo = None
		htmlContent = requests.get(self.url, timeout = self.timeout)
		if htmlContent.status_code == 200:
			try:
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
			except Exception as e:
				log.error(f'Song are not fetched successfully from spotify. Exception is {e}')
		return spotifyInfo


	def getSongNameAndArtistInString(self, track):
		songName = track.get('name')
		artists = track.get('artists', [])
		try:
			artistsInString = ' '.join(map(lambda artist: artist['name'], artists))
			return f'{songName} - {artistsInString}'
		except Exception as e:
			log.error(f'Info fetched from spotify is not valid. Exception is {e}. Info is {track}')
			return None


	def getSongFromList(self, spotifyInfo):
		if 'tracks' in spotifyInfo:
			try:
				songNameList = []
				playlistInDict = spotifyInfo.get('tracks', {}).get('items', [])
				for trackContainer in playlistInDict:
					track = trackContainer['track']
					songName = self.getSongNameAndArtistInString(track)
					if songName is not None and 'uri' in track:
						songNameList.append((songName, track['uri']))
				return songNameList
			except Exception as e:
				log.error(
					f'Invalid spotify info while fetching playlist. Exception is {e}. Spotify info is {spotifyInfo}')
		else:
			return None


	def getSongFromAlbum(self, spotifyInfo):
		if 'tracks' in spotifyInfo:
			try:
				songNameList = []
				playlistInDict = spotifyInfo.get('tracks', {}).get('items', [])
				for track in playlistInDict:
					songName = self.getSongNameAndArtistInString(track)
					if songName is not None and 'uri' in track:
						songNameList.append((songName, track['uri']))
				return songNameList
			except Exception as e:
				log.error(
					f'Invalid spotify info while fetching playlist. Exception is {e}. Spotify info is {spotifyInfo}')
		else:
			return None


	def getUrlType(self):
		if 'track' in self.url:
			return SpotifyFetcher.UrlType.TRACK
		elif 'playlist' in self.url:
			return SpotifyFetcher.UrlType.PLAYLIST
		elif 'album' in self.url:
			return SpotifyFetcher.UrlType.ALBUM
		else:
			return None
