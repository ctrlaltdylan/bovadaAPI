import os
from error import BovadaException
import requests
from was_successful import was_successful
from headers import get_bovada_headers_generic, get_bovada_headers_authorization
from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
from Parser import parse_response, parse_special_response
import json
#from BovadaMatches import SoccerMatches, BasketballMatches, BaseballMatches, TennisMatches, RugbyMatches

all_urls = []
response_objects =[]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))






def bind_api(auth_obj, action, *args, **kwargs):
	
	bovada_match_file = os.path.join(BASE_DIR, "bmatches.json")
	try:	
		with open(bovada_match_file, 'r') as infile:
			all_matches = json.loads(infile)
	except IOError:
		pass
	else:
		return all_matches
	soccer_matches = []
	basketball_matches = []
	baseball_matches = []
	tennis_matches = []
	rugby_matches = []
	football_matches = []
	try:
		amount_to_deposit = kwargs.pop("amount")
	except KeyError:
		amount_to_deposit = None
	try:
		outcomeId = kwargs.pop("outcomeId")
	except KeyError:
		outcomeId = None

	urls_to_scrape = []
	profile_id = auth_obj._auth["profile_id"]
	access_token = auth_obj._auth["access_token"]
	token_type = auth_obj._auth["token_type"]
	expiration_date = auth_obj._auth["expiration_date"]
	if action == "summary" or action=="wallets" or action=="deposit" or action=="place_bets":
		headers = get_bovada_headers_authorization(access_token, token_type)
	else:
		headers = get_bovada_headers_generic()
	request = requests.get(get_endpoint(action=action, profile_id=profile_id, outcomeId=outcomeId), headers=headers)
	if was_successful(request):
		if action == "summary" or action =="wallets" or action=="deposit":
			return parse_special_response(request)
		elif action == "place_bets":
			return validate_bets(bets, channel, groups, selections)
		else:
			query_all_endpoints = find_relative_urls(request)
			print "number of requests {}".format(len(all_urls))
			print "number of responses {}".format(len(response_objects))
			for obj in response_objects:
				#this is where we actually get the bovada matches on each page
				bmatches = parse_response(obj)
				if bmatches:
					for match in bmatches: 
						if match.sport == "BASK":
							if (match.home_team_full_name not in [x.home_team_full_name for x in basketball_matches] and
								match.away_team_full_name not in [away_team.away_team_full_name for away_team in basketball_matches]):
									basketball_matches.append(match)

						elif match.sport == "FOOT":
							if(match.home_team_full_name not in [z.home_team_full_name for z in football_matches] and
								match.away_team_full_name not in [t.away_team_full_name for t in football_matches]):
									football_matches.append(match)

						elif match.sport == "BASE":
							if (match.home_team_full_name not in [p.home_team_full_name for p in basketball_matches] and 
								match.away_team_full_name not in [j.away_team_full_name for j in basketball_matches]):
									basketball_matches.append(match)

						elif match.sport == "TENN":
							if (match.home_team_full_name not in [n.home_team_full_name for n in tennis_matches] and
								match.away_team_full_name not in [m.away_team_full_name for m in tennis_matches]):
									tennis_matches.append(match)

						elif match.sport == "RUGBU":
							if (match.home_team_full_name not in [s.home_team_full_name for s in rugby_matches] and
								match.away_team_full_name not in [l.away_team_full_name for l in rugby_matches]):
									rugby_matches.append(match)
			return {
				"basketball_matches": basketball_matches,
				"baseball_matches": baseball_matches,
				"rugby_matches": rugby_matches,
				"football_matches":football_matches,
				"soccer_matches":soccer_matches,
				"tennis_matches": tennis_matches,
			}
	else:
		raise BovadaException(request.reason)




def find_relative_urls(response, index=1):
	#append the response object to response_objects list so we dont have to make any queries again.
	if response.json() not in response_objects:
		response_objects.append(response.json())
	if response.url not in all_urls:
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
def get_endpoint(action, profile_id, outcomeId=None):
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

	elif action == "football_matches":
		endpoint = "https://sports.bovada.lv/football?json=true"

	elif action == "tennis_matches":
		endpoint = "https://sports.bovada.lv/tennis?json=true"

	elif action == "rugby_matches":
		endpoint = "https://sports.bovada.lv/rugby-union?json=true"

	elif action == "baseball_matches":
		endpoint = "https://sports.bovada.lv/baseball?json=true"

	elif action == "place_bets":
		if not outcomeId:
			raise BovadaException("can't place a bet without the outcome id")
		else:
			#format https://sports.bovada.lv/services/sports/bet/betslip?outcomeId=A:91769724:1&outcomeId=A:91769726:2
			endpoint = "https://sports.bovada.lv/services/sports/bet/betslip?outcomeId={}"
	
	else:
		raise BovadaException("did not receive a valid action. Received: {}".format(action))
	return endpoint

