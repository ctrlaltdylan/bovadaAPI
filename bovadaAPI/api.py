from auth import login_to_bovada
from selenium.webdriver import Firefox
from .error import BovadaException
from .decorators import authentication_required, authentication_recommended




class BovadaApi(object):

	def __init__(self, authentication=None,driver=None, *args, **kwargs):
		self.authentication = authentication
		self.driver = Firefox()
		self.current_url = "https://bovada.lv"
		return super(BovadaApi, self).__init__(*args, **kwargs)


	def authenticate(self):
		try:
			logged_in = login_to_bovada(self)
		except Exception, e:
			print e

		
	
	@authentication_required
	@property
	def balance(self):
		return bind_api(action="balance")


	@authentication_required
	@property
	def bet_history(self):
		self.current_url = "https://www.bovada.lv/?pushdown=bet-history"
		return bind_api(action="bet_history")

	@authentication_required
	@property
	def open_bets(self):
		self.current_url = "https://www.bovada.lv/?pushdown=bet-history"
		return bind_api(action="open_bets")

	@authentication_recommended
	@property
	def soccer_matches(self):
		self.current_url = "https://sports.bovada.lv/soccer"
		return bind_api(action="soccer_matches")

	@authentication_recommended
	@property
	def basketball_matches(self):
		self.current_url = "https://sports.bovada.lv/basketball"
		return bind_api(action="basketball_matches")
	
	@authentication_recommended
	@property
	def tennis_matches(self):
		self.current_url = "https://sports.bovada.lv/tennis"
		return bind_api(action="tennis_matches")

	@authentication_recommended
	@property
	def rugby_matches(self):
		self.current_url = "https://sports.bovada.lv/rugby"
		return bind_api(action="rugby_matches")

	


