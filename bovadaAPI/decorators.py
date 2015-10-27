from error import BovadaException




def authentication_required(func):
	def authentication_wrapper(self):
		print self.authentication
		if self.authentication == None:
			raise BovadaException("You must be authenticated with bovada to use this function")
	return authentication_wrapper



def bovada_api(func):
	def bovada_api_wrapper(self, *args, **kwargs):
		driver = self.driver
		driver.get(self.current_url)
		return func(driver=driver, *args, **kwargs)
	return bovada_api_wrapper


def authentication_recommended(func):
	def authentication_reccommended_wrapper(self, *args, **kwargs):
		if self.authentication == None:
			print "Not authenticating first will mean the odds will be in American Format"
	return authentication_recommended

