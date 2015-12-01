#Created By: Jon Kolman
#version: 1.0
#description: An API to interact with https://bovada.lv. 
import os
from cached_property import cached_property
from auth import login_to_bovada
from error import BovadaException, BovadaAuthenticationError
from decorators import authentication_required, authentication_recommended
from bind_api import bind_api
from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
import requests
import json
import datetime



class BovadaApi(object):

	def __init__(self, *args, **kwargs):
		self._auth = None
		return super(BovadaApi, self).__init__(*args, **kwargs)

	@property
	def auth(self):
		try:
			response = login_to_bovada()
		except Exception, e:
			raise BovadaAuthenticationError(e)
		else:
			cookies = dict()
			for cookie in response.cookies:
				cookies[cookie.name] = cookie.value
			self._auth = response.json()
			self._auth['profile_id'] = response.headers['X-Profile-Id']
			self._auth['expiration_date'] = self._get_expiration_time(self._auth['expires_in'])
			self._auth["cookies"] = cookies
			return self._auth
		

		
	
	@property
	@authentication_required
	def summary(self):
		return bind_api(self, action="summary")

	@property
	@authentication_required
	def balance(self):
		return bind_api(self, action="balance")

	@property
	@authentication_required
	def bet_history(self):
		return bind_api(self, action="bet_history")

	@property
	@authentication_required
	def open_bets(self):
		return bind_api(self, action="open_bets")

	@cached_property
	@authentication_recommended
	def soccer_matches(self):
		return bind_api(self, action="soccer_matches")['soccer_matches']

	@cached_property
	@authentication_recommended
	def basketball_matches(self):
		return bind_api(self, action="basketball_matches")['basketball_matches']
	
	@cached_property
	@authentication_recommended
	def tennis_matches(self):
		return bind_api(self, action="tennis_matches")['tennis_matches']

	@cached_property
	@authentication_recommended
	def rugby_matches(self):
		return bind_api(self, action="rugby_matches")['rugby_matches']

	@cached_property
	@authentication_recommended
	def football_matches(self):
		return bind_api(self, action="football_matches")['football_matches']

	
	@cached_property
	@authentication_recommended
	def baseball_matches(self):
		return bind_api(self, action="baseball_matches")['baseball_matches']
	#generates an expiration time obj by adding the fast_forward amount to the current time
	def _get_expiration_time(self, fast_forward):
		pass

	@authentication_required
	#endpoint = https://sports.bovada.lv/services/sports/bet/betslip/validate
	def validate_bets(self, bets):
		return bind_api(self, action="validate_bets", bets=bets)

	@authentication_required
	def place_bets(self, *args):
		#https://sports.bovada.lv/services/sports/bet/betslip/c7a970f8-37ca-39dd-ab5f-69fb560aea42
		return bind_api(action="place_bets", *args)

	@authentication_required
	def deposit(self, amount):
		return bind_api(self, action="deposit", amount=amount)

	@property
	@authentication_required
	def wallet(self):
		return bind_api(self, action="wallets")

	

def stream():
	import time
	while True:

		b = BovadaApi()
		b.auth
		print "balance {}".format(b.balance)
		print "\n"
		print "open_bets {}".format(b.open_bets)
		print "\n"
		print "bet_history {}".format(b.bet_history)
		time.sleep(100)







