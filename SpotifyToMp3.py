import sys

from PySide2 import QtWidgets

from mainWindow import MainWindow

reload( sys )
sys.setdefaultencoding( 'utf8' )
if __name__ == "__main__":
	# setup app

	# setup Qt app for ui
	app = QtWidgets.QApplication( sys.argv )
	app.setApplicationName( "SpotifyToMp3" )

	# setup ui
	mainWindow = MainWindow()
	mainWindow.show()

	sys.exit( app.exec_() )
