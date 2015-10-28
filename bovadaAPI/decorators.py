from error import BovadaException




def authentication_required(func):
	def authentication_wrapper(self, *args, **kwargs):
		if self._auth == None:
			raise BovadaException("You must be authenticated with bovada to use this function")
		else:
			return func(self, *args, **kwargs)
	return authentication_wrapper





def authentication_recommended(func):
	def authentication_reccommended_wrapper(self, *args, **kwargs):
		if self._auth == None:
			print "Not authenticating first will mean the odds will be in American Format"
		return func(self, *args, **kwargs)
	return authentication_reccommended_wrapper

