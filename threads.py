from time import sleep

from PySide2 import QtCore, QtWidgets


class Thread( QtCore.QThread ):
	successful = QtCore.Signal( object )
	failed = QtCore.Signal( str )
	update = QtCore.Signal( object )

	def __init__( self, func, dialog = False, parent = None, **kwargs ):
		super( Thread, self ).__init__( parent )
		self.params = kwargs
		self.openDialog = dialog
		self.func = func

	def setParams( self, **kwargs ):
		self.params = kwargs

	def run( self ):
		try:
			if self.openDialog:
				self.params['dialog'] = self.dialog
			self.params['updateSignal'] = self.update
			value = self.func( **self.params )
		except Exception, e:
			self.failed.emit( str( e ) )
			return False
		self.successful.emit( value )
		return True

	def start( self, **kwargs ):
		self.params = kwargs
		if self.openDialog:
			self.dialog.open()
		super( Thread, self ).start()
