import os
from error import BovadaException, BovadaAuthenticationError
from was_successful import was_successful
from headers import get_bovada_headers_generic
import requests
import json
import time


def login_to_bovada():
	"""on purpose I kept the login flow the same as if you were logging into Bovada using a browser.
		I could have just queried the api/token endpoint directly, but figured that may raise some
		flags with bovada since the login process would be skipping a step. 
	"""
	query_1 = query_login_endpoint() #query the login endpoint like we would if using a browser
	if query_1.status_code == 200:
		authenticated_ourselves = bovada_auth()
		if authenticated_ourselves.status_code == 200:
			return authenticated_ourselves
		else:
			raise BovadaAuthenticationError(authenticated_ourselves.reason)
	else:
		raise BovadaException(query_1.reason)



def query_login_endpoint():
	return requests.get("https://www.bovada.lv/websites/services/components/login")
	

def bovada_auth():
	try:
		username = os.environ["BOVADA_USERNAME"]
	except KeyError:
		raise BovadaException("could not find your bovada username. Did you export it as an environment variable?")
	try:
		password = os.environ["BOVADA_PASSWORD"]
	except KeyError:
		raise BovadaException("Could not find your bovada password. Did you export it as an environment variable?")
	
	payload = json.dumps({
		"username": username, 
		"password":password})
	return requests.post("https://www.bovada.lv/services/web/v2/oauth/token", 
		data=payload, 
		headers=get_bovada_headers_generic())
