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
	""" A class to interface with https://bovada.lv 
		The methods defined in here send an action to the bind_api() which consequently 
		sends the appropriate http get request or post request to a specific bovada.lv endpoint
		By default auth credentials is set to None. To use account specific functions like
		balance, summary, bet_history or open bets you must export a BovadaUsername and a BovadaPassword
	"""

	def __init__(self, *args, **kwargs):
		self._auth = None
		return super(BovadaApi, self).__init__(*args, **kwargs)

	@property
	def auth(self):
		"""
		attemps to login to bovada with exports BovadaUsername and Password
		if the request is successfull, all subsequent requests will use the cookies
		and headers that were sent back from bovada. 
		"""
		try:
			login = login_to_bovada()
		except Exception, e:
			raise BovadaAuthenticationError(e)
		else:
			cookies = dict()
			for cookie in login.cookies:
				cookies[cookie.name] = cookie.value
			self._auth = login.json()
			self._auth['profile_id'] = login.headers['X-Profile-Id']
			self._auth["cookies"] = cookies
			return self._auth
		

		
	
	@property
	@authentication_required
	
	def summary(self):
		"""this returns your account summary
		"""
		return bind_api(self, action="summary")

	@property
	@authentication_required
	def balance(self):
		"""this returns your current balance as an int"""
		return bind_api(self, action="balance")

	@property
	@authentication_required
	def bet_history(self):
		"""this returns your bet_history """
		return bind_api(self, action="bet_history")

	@property
	@authentication_required
	def open_bets(self):
		"""this returns your open bets"""
		return bind_api(self, action="open_bets")


	@authentication_recommended
	def soccer_matches(self):
		""" this returns all soccer matches
			the first url to be queried is https://sports.bovada.lv/soccer/
			then all subsequent urls are queried and scraped to return all soccer matches
			currently on bovada. If that's not dope, I don't know what is.
		"""
		return bind_api(self, action="soccer_matches")['soccer_matches']


	@authentication_recommended
	def basketball_matches(self):
		"""
			the first url to be queried is https://sports.bovada.lv/basketball/
			then all subsequent urls are queried and scraped to return all basketball matches
			currently on bovada. If that's not dope, I don't know what is.
		"""
		return bind_api(self, action="basketball_matches")['basketball_matches']
	

	@authentication_recommended
	def tennis_matches(self):
		"""
			the first url to be queried is https://sports.bovada.lv/tennis/
			then all subsequent urls are queried and scraped to return all tennis matches
			currently on bovada. If that's not dope, I don't know what is.
		"""

		return bind_api(self, action="tennis_matches")['tennis_matches']


	@authentication_recommended
	def rugby_matches(self):
		"""
			the first url to be queried is https://sports.bovada.lv/rugby-union/
			then all subsequent urls are queried and scraped to return all rugby matches
			currently on bovada. If that's not dope, I don't know what is.
		"""
		return bind_api(self, action="rugby_matches")["rugby_matches"]


	@authentication_recommended
	def football_matches(self):
		"""
			the first url to be queried is https://sports.bovada.lv/football/
			then all subsequent urls are queried and scraped to return all football matches
			currently on bovada. If that's not dope, I don't know what is.
		"""
		return bind_api(self, action="football_matches")['football_matches']

	

	@authentication_recommended
	def baseball_matches(self):
		"""
			the first url to be queried is https://sports.bovada.lv/baseball/
			then all subsequent urls are queried and scraped to return all baseball matches
			currently on bovada. If that's not dope, I don't know what is.
		"""
		return bind_api(self, action="baseball_matches")['baseball_matches']
	


	

def stream():
	""" a fun function to run that periodiclly checks to see how much money you're up,
	by comparing your bet history """
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







