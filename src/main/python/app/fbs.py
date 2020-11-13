import os
from fbs_runtime.application_context.PySide2 import ApplicationContext


class BaseApplicationContext(ApplicationContext):
	def __init__(self):
		super(BaseApplicationContext, self).__init__()


	def qss(self, filename):
		try:
			file = open(self.get_resource(os.path.join('qss', filename)))
			qss = file.read()
			return qss
		except Exception as e:
			return None


	def icons(self, iconName = ''):
		try:
			return self.get_resource(os.path.join('icons', iconName))
		except Exception as e:
			return None
