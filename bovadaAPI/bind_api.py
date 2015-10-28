from .error import BovadaException
import requests
from was_successful import was_successful
from headers import get_bovada_headers_generic, get_bovada_headers_authorization
#from BovadaMatches import SoccerMatches, BasketballMatches, BaseballMatches, TennisMatches, RugbyMatches





def bind_api(auth_obj, action):
	profile_id = auth_obj.auth["profile_id"]
	access_token = auth_obj.auth["access_token"]
	token_type = auth_obj.auth["token_type"]
	expiration_date = auth_obj.auth["expiration_date"]
	if action == "summary":
		headers = get_bovada_headers_authorization(access_token, token_type)
	else:
		headers = get_bovada_headers_generic()
	request = requests.get(get_endpoint(action=action, profile_id=profile_id), headers=headers)
	if was_successful(request):
		return request.json()





def get_endpoint(action, profile_id):
	if  action == "soccer_matches":
		endpoint = "https://sports.bovada.lv/soccer?json=true"

	elif action == "summary":
		 endpoint = "https://www.bovada.lv/services/web/v2/profiles/%s/summary" % profile_id



	elif action == "basketball_matches":
		endpoint = "https://sports.bovada.lv/basketball?json=true"

	elif action == "tennis_matches":
		endpoint = "https://sports.bovada.lv/tennis?json=true"

	elif action == "rugby_matches":
		endpoint = "https://sports.bovada.lv/rugby?json=true"
	

	elif action == "baseball_matches":
		endpoint = "https://sports.bovada.lv/baseball?json=true"
	
	else:
		raise BovadaException("did not receive a valid action. Received: {}".format(action))
	return endpoint