import json

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
								return metaData

			return None


class SpotifyFetcher(BaseFetcher):
	def __init__(self, url, timeout):
		super(SpotifyFetcher, self).__init__()
		self.url = url
		self.timeout = timeout


	def fetchContent(self):
		songInDict = self.getSongListInDict()
		if songInDict is not None:
			return self.getSongNameAndArtistInString(songInDict)
		else:
			return None


	def getSongListInDict(self):
		spotifyInfo = None
		htmlContent = requests.get(self.url, timeout = self.timeout)
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
