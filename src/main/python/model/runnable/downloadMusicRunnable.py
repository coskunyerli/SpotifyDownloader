import os

import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets
import youtube_dl
from model.runnable.baseRunnable import BaseRunnable
from model.stopThreadSignal import StopThreadSignal


class DownloadMusicRunnable(QtCore.QObject, BaseRunnable):
	update = QtCore.Signal(object)
	successful = QtCore.Signal()
	failed = QtCore.Signal(str)
	finished = QtCore.Signal()


	def __init__(self, songIndexes, outputFolderPath):
		QtCore.QObject.__init__(self)
		BaseRunnable.__init__(self)
		self.__stopSignal = StopThreadSignal()
		self.__outputFolderPath = outputFolderPath
		self.__songIndexes = songIndexes


	def run(self):
		try:
			path = os.path.join(self.__outputFolderPath, '%(title)s.%(ext)s)')
			download_options = {
				'format': 'bestaudio/best',
				'outtmpl': path,
				'nocheckcertificate': True,
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
				}],
			}
			lenght = len(self.__songIndexes)
			step = 100.0 / lenght
			with youtube_dl.YoutubeDL(download_options) as dl:
				for i in range(lenght):
					if self.__stopSignal.isStopped():
						return
					songs = self.__songIndexes[i]
					song = songs.currentItem()
					self.update.emit((song.name, i * step))
					dl.download([f'https://www.youtube.com/watch?v={song.id}'])

			self.successful.emit()
		except Exception as e:
			self.failed.emit(f'Download music process is failed. Exception is {str(e)}')
		finally:
			self.finished.emit()


	def stop(self):
		self.__stopSignal.stop(True)
