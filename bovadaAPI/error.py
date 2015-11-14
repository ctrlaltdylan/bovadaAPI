import six





class BovadaException(object):

	def __init__(self, reason, response=None):
		self.reason = six.text_type(reason)
		self.response = response
		Exception.__init__(self, reason)

	def __str__(self):
		return self.reason


class BovadaAuthenticationError(BovadaException):
	#Bovada Authentication Error has the exact same properties
	#as Bovada Exception for backwards compatibility reasons
	pass


