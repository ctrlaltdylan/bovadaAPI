from error import BovadaException
import requests
from was_successful import was_successful
from headers import get_bovada_headers_generic, get_bovada_headers_authorization
from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
import json
#from BovadaMatches import SoccerMatches, BasketballMatches, BaseballMatches, TennisMatches, RugbyMatches

all_urls = []
response_objects =[]



class BovadaMatch(object):
	def __init__(self, *args, **kwargs):
		self.sport = kwargs.pop("sport")
		self.description = kwargs.pop("description")
		self.startTime = kwargs.pop("startTime")
		self.home_team_short_name = kwargs.pop("home_team_short_name")
		self.home_team_full_name = kwargs.pop("home_team_full_name")
		self.home_team_abbreviation = kwargs.pop("home_team_abbreviation")
		self.away_team_short_name = kwargs.pop("away_team_shortname")
		self.away_team_full_name = kwargs.pop("away_team_full_name")
		self.away_team_abbreviation= kwargs.pop("away_team_abbreviation")
		self.game_link = kwargs.pop("game_link")
		self.type = kwargs.pop("type")
		self.game_id = kwargs.pop("game_id")
		self.outcomes = kwargs.pop("outcomes")
		return super(BovadaMatch, self).__init__()

	@property
	def match_details(self):
		return "%s, %s, %s, %s, %s, %s, %s, %s" %(self.sport, self.game_link, 
			self.description, self.startTime, self.home_team_full_name,
			self.game_link, self.type, self.game_id)

class Odds(object):
	def __init__(self, *args, **kwargs):
		self.odds_type = kwargs.pop("odds_type")
		return super(Odds, self).__init__(*args, **kwargs)
	


class OutCome(object):
	def __init__(self, *args, **kwargs):
		self.parent = kwargs.pop("parent")
		self.name = kwargs.pop("name")
		self.price = kwargs.pop("price")
		return super(OutCome, self).__init__(*args, **kwargs)


def bind_api(auth_obj, action, *args, **kwargs):
	try:
		amount_to_deposit = kwargs.pop("amount")
	except KeyError:
		amount_to_deposit = None
	urls_to_scrape = []
	profile_id = auth_obj._auth["profile_id"]
	access_token = auth_obj._auth["access_token"]
	token_type = auth_obj._auth["token_type"]
	expiration_date = auth_obj._auth["expiration_date"]
	if action == "summary" or action=="wallets" or action=="deposit":
		headers = get_bovada_headers_authorization(access_token, token_type)
	else:
		headers = get_bovada_headers_generic()
	request = requests.get(get_endpoint(action=action, profile_id=profile_id), headers=headers)
	if was_successful(request):
		if action == "summary" or action =="wallets" or action=="deposit":
			return parse_special_response(request)
		else:
			query_all_endpoints = find_relative_urls(request)
			print len(all_urls)
			print len(response_objects)
			

			






def was_successful(request):
	print "calling was_successful"
	if request.status_code == 200:
		return True
	else:
		return False




def find_relative_urls(response, index=1):
	#append the response object to response_objects list so we dont have to make any queries again.
	response_objects.append(response.json())
	all_urls.append(response.url)
	try:
		url_list = [x['relativeUrl'] for x in response.json()['data']['page']['navigation']['navigation'][index]['items']]
	except (IndexError, KeyError, TypeError):
		url_list = None
		pass
	if url_list:
		for url in url_list:
			page = get_relative_url(url)
			if page:
				find_relative_urls(page, index=index+1)
		return all_urls
	return all_urls

def get_relative_url(endpoint):
	URL = "https://sports.bovada.lv{}?json=true".format(endpoint)
	try:
		response = requests.get(URL, headers=get_bovada_headers_generic())
	except:
		response = None
		return response
	if was_successful(response):
		#save our response objects in memory so we dont have to query again.
		response_objects.append(response.json())
		return response
def get_endpoint(action, profile_id):
	if  action == "soccer_matches":
		endpoint = "https://sports.bovada.lv/soccer?json=true"

	elif action == "summary":
		 endpoint = "https://www.bovada.lv/services/web/v2/profiles/%s/summary" % profile_id

	elif action == "deposit":
		endpoint = "https://www.bovada.lv/?pushdown=cashier.deposit"

	elif action == "wallets":
		endpoint = "https://www.bovada.lv/services/web/v2/profiles/%s/wallets" % profile_id

	elif action == "basketball_matches":
		endpoint = "https://sports.bovada.lv/basketball?json=true"

	elif action == "tennis_matches":
		endpoint = "https://sports.bovada.lv/tennis?json=true"

	elif action == "rugby_matches":
		endpoint = "https://sports.bovada.lv/rugby-union?json=true"

	elif action == "baseball_matches":
		endpoint = "https://sports.bovada.lv/baseball?json=true"
	
	else:
		raise BovadaException("did not receive a valid action. Received: {}".format(action))
	return endpoint

