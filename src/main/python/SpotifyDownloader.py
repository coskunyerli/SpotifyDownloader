import os

from fbs_runtime.application_context.PySide2 import ApplicationContext
from mainWindow import MainWindow

import sys

from widgets.toast import Toast

if __name__ == '__main__':
	fbs = ApplicationContext()  # 1. Instantiate ApplicationContext
	# setup ui

	Toast.settings['iconsPath'] = fbs.get_resource(os.path.join('icons', 'toast'))
	mainWindow = MainWindow()
	Toast.setWidget(mainWindow)

	mainWindow.show()
	exit_code = fbs.app.exec_()  # 2. Invoke appctxt.app.exec_()
	sys.exit(exit_code)
