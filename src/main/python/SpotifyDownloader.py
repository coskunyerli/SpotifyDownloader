from fbs_runtime.application_context.PySide2 import ApplicationContext
from mainWindow import MainWindow

import sys

if __name__ == '__main__':
	appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
	# setup ui
	mainWindow = MainWindow()
	mainWindow.show()
	exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
	sys.exit(exit_code)
