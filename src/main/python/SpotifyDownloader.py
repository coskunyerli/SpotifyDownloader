import os
import traceback

import log
from app.fbs import BaseApplicationContext

import sys
import PySide2.QtWidgets as QtWidgets

if __name__ == '__main__':
	fbs = BaseApplicationContext()  # 1. Instantiate ApplicationContext
	# setup ui
	try:
		log.init(fbs.get_resource())
	except Exception as e:
		QtWidgets.QMessageBox.critical(None, 'Log Create Error', f'Log file is not created successfully. Error is {e}')
		exit(-1)

	exit_code = 1
	try:
		from widgets.toast import Toast
		from mainWindow import MainWindow

		Toast.settings['iconsPath'] = fbs.get_resource(os.path.join('icons', 'toast'))
		mainWindow = MainWindow()
		mainWindowQss = fbs.qss('mainWindow.qss')
		if mainWindowQss is not None:
			mainWindow.setStyleSheet(mainWindowQss)
		else:
			log.warning(f'Main window qss is not loaded successfully')

		Toast.setWidget(mainWindow)

		mainWindow.show()
		exit_code = fbs.app.exec_()  # 2. Invoke appctxt.app.exec_()
		sys.exit(exit_code)
	except Exception as e:
		traceback.print_exc()
		log.critical("Unexpected Error, " + str(e))
		QtWidgets.QMessageBox.critical(None, "Unexpected Error", str(e))
	finally:
		sys.exit(exit_code)
