from ghost import Ghost
from .error import BovadaException
from .decorators import authentication_required




class BovadaApi(object):

	def __init__(self, authentication=None,driver=None, *args, **kwargs):
		self.authentication = authentication
		self.driver = Ghost()
		return super(BovadaApi, self).__init__(*args, **kwargs)


	@property
	def authenticate(self, username, password):
		pass

	
	@authentication_required
	@property
	def get_bovada_balance(self):
		pass


	@authentication_required
	@property
	def get_bet_history(self):
		pass

	@authentication_required
	@property
	def get_open_bets(self):
		pass

	@property
	def get_all_soccer_matches(self):
		pass

	@property
	def get_all_basketball_matches(self):
		pass

	@property
	def get_all_tennis_matches(self):
		pass

	@property
	def get_all_rugby_matches(self):
		pass

	def start_session(self, authenticated_session=False):
		if authenticated_session == False:
			with self.driver.start() as session:
				page, resources = session.open("http://bovada.lv")
				assert page.http_status == 200 and "bovada" in page.content



