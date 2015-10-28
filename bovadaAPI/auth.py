from django.conf import settings
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
	payload = json.dumps({
		"username": settings.BOVADA_USERNAME, 
		"password":settings.BOVADA_PASSWORD})
	return requests.post("https://www.bovada.lv/services/web/v2/oauth/token", 
		data=payload, 
		headers=get_bovada_headers_generic())
