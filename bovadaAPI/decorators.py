from error import BovadaException




def authentication_required(func):
	def authentication_wrapper(self):
		print self.authentication
		if self.authentication == None:
			raise BovadaException("You must be authenticated with bovada to use this function")
	return authentication_wrapper
