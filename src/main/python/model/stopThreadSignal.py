class StopThreadSignal(object):
	def __init__(self):
		self.__isStopped = False


	def stop(self, res):
		self.__isStopped = res


	def isStopped(self):
		return self.__isStopped
