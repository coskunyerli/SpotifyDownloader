import datetime
import logging
import os

INFO = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR
WARNING = logging.WARNING


def init(path):
	logName = datetime.datetime.now().strftime("%m-%d-%Y.log")
	# check path exists or not. I not exists create it
	logPath = os.path.join(path, 'log')
	if os.path.exists(logPath) is False:
		os.mkdir(logPath)
	basicConfig(filename = os.path.join(logPath, logName),
				format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = INFO)


def warning(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.warning(msg)


def info(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.info(msg)


def error(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.error(msg)


def critical(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.critical(msg)


def basicConfig(*args, **kwargs):
	logging.basicConfig(*args, **kwargs)
