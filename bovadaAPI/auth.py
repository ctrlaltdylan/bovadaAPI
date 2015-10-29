import os
from error import BovadaException, BovadaAuthenticationError
from was_successful import was_successful
from headers import get_bovada_headers_generic
import requests
import json
import time


def login_to_bovada():
	query_1 = query_login_endpoint() #query the login endpoint like we would if using a browser
	if was_successful(query_1):
		query_2 = bovada_auth()
		if was_successful(query_2):
			return query_2
		else:
			raise BovadaAuthenticationError(query_2.reason)
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
		"username": username 
		"password":password})
	return requests.post("https://www.bovada.lv/services/web/v2/oauth/token", 
		data=payload, 
		headers=get_bovada_headers_generic())
