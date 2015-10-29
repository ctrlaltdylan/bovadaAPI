#Created By: Jon Kolman
#version: 1.0
#description: An API to interact with https://bovada.lv. 
import os
from cached_property import cached_property
from auth import login_to_bovada
from .error import BovadaException
from .decorators import authentication_required, authentication_recommended
from bind_api import bind_api
import json
import datetime



class BovadaApi(object):

	def __init__(self, *args, **kwargs):
		self._auth = None
		return super(BovadaApi, self).__init__(*args, **kwargs)

	@cached_property
	def auth(self):
		try:
			response = login_to_bovada()
		except Exception, e:
			print e
		else:
			self._auth = response.json()
			self._auth['profile_id'] = response.headers['X-Profile-Id']
			self._auth['expiration_date'] = self._get_expiration_time(self._auth['expires_in'])
			return self._auth
		


		
	
	@property
	@authentication_required
	def summary(self):
		return bind_api(self, action="summary")

	@property
	@authentication_required
	def balance(self):
		print "balance called"
		return bind_api(self, action="balance")

	@property
	@authentication_required
	def bet_history(self):
		return bind_api(self, action="bet_history")

	@property
	@authentication_required
	def open_bets(self):
		return bind_api(self, action="open_bets")

	@property
	@authentication_recommended
	def soccer_matches(self):
		return bind_api(self, action="soccer_matches")

	@property
	@authentication_recommended
	def basketball_matches(self):
		return bind_api(self, action="basketball_matches")
	
	@property
	@authentication_recommended
	def tennis_matches(self):
		return bind_api(self, action="tennis_matches")

	@property
	@authentication_recommended
	def rugby_matches(self):
		return bind_api(self, action="rugby_matches")

	
	#generates an expiration time obj by adding the fast_forward amount to the current time
	def _get_expiration_time(self, fast_forward):
		pass




