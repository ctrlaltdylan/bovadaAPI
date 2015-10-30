from error import BovadaException
import requests
from was_successful import was_successful
from headers import get_bovada_headers_generic, get_bovada_headers_authorization
from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
#from BovadaMatches import SoccerMatches, BasketballMatches, BaseballMatches, TennisMatches, RugbyMatches

all_bmatches = []
#all_outcome_objects = []
#all_odds_objects = []


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


def bind_api(auth_obj, action):
	profile_id = auth_obj._auth["profile_id"]
	access_token = auth_obj._auth["access_token"]
	token_type = auth_obj._auth["token_type"]
	expiration_date = auth_obj._auth["expiration_date"]
	if action == "summary":
		headers = get_bovada_headers_authorization(access_token, token_type)
	else:
		headers = get_bovada_headers_generic()
	request = requests.get(get_endpoint(action=action, profile_id=profile_id), headers=headers)
	if was_successful(request):
		return parse_response(request.json())
		



def parse_response(response):
	#store our relative urls here. Get these urls and parse their pages after parsing current page.
	rel_urls = find_relative_urls(response)
	bmatches = []
	center_content = response['data']['regions']['content_center'] #useful
	market_lines =  search_dictionary_for_certain_keys("value", [value for value in response['data']['regions']['content_center'].values()][0])#other keys = name, value#returns odds ['json-var']['value']
	gamelines = search_dictionary_for_certain_keys("items", center_content)[0] #index 0 is gamelines index 1 is futures
	for match in gamelines['itemList']['items']:
		outcome_objects_for_match = []
		game_sport = str(match['sport'])
		game_id = int(match['id'])
		description = str(match['description'])
		startTime = str(match['startTime'])
		competitors = match['competitors']
		home_team_abbreviation = search_dictionary_for_certain_keys("abbreviation", competitors[1])
		home_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[1])
		home_team_full_name = search_dictionary_for_certain_keys("description", competitors[1])
		away_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[0])
		away_team_abbreviation=  search_dictionary_for_certain_keys("abbreviation", competitors[0])
		away_team_full_name = search_dictionary_for_certain_keys("description", competitors[0])
		game_link = "https://sports.bovada.lv{}".format(str(match['link']))
		type_ = match['type']
		displayGroups= match['displayGroups']
		for group in displayGroups:
			if group['description'] != "Game Lines":
				pass
			else:
				betting_lines = [x for x in group["itemList"]]
				for line in betting_lines:
					odds_type = line['description']
					outcomes = line['outcomes']
					odds_obj = Odds(odds_type=odds_type)
					for outcome in outcomes:
						name = outcome['description']
						try:
							price  = outcome['price']["decimal"]
						except KeyError:
							price = None
						outcome_obj = OutCome(parent=odds_obj, 
							name=name, 
							price=price)
						outcome_objects_for_match.append(outcome_obj)


					

		bmatch = BovadaMatch(
				sport=game_sport,
				description=description,
				startTime=startTime,
				home_team_short_name=home_team_short_name,
				home_team_full_name = home_team_full_name,
				home_team_abbreviation = home_team_abbreviation,
				away_team_shortname = away_team_short_name,
				away_team_abbreviation = away_team_abbreviation,
				away_team_full_name = away_team_full_name,
				game_link=game_link,
				type=type_,
				game_id=game_id, 
				outcomes=outcome_objects_for_match)
		all_bmatches.append(bmatch)
		bmatches.append(bmatch)
			
	try:
		already_parsed_endpoints = [x['link'] for x in market_lines['items']] #no need to query these urls again
	except TypeError:
		already_parsed_endpoints = []

	# if rel_urls:
	# 	for url in rel_urls:
	# 		if url not in already_parsed_endpoints:
	# 			response = requests.get("https://sports.bovada.lv"+url, headers=get_bovada_headers_generic())
	# 			if was_successful(response):
	# 				return parse_response(response.content)
	# 				try:
	# 					response_as_json = response.json()
	# 				except ValueError, e:
	# 					response_as_json = None
	# 				else:
	# 					if response_as_json:
	# 						return parse_response(response_as_json)


	# 			else:
	# 				raise BovadaException("connection to endpoint {} failed".format(url))
	# else:
	return all_bmatches





def was_successful(request):
	print "calling was_successful"
	if request.status_code == 200:
		return True
	else:
		return False


def find_relative_urls(response):
	return [x['relativeUrl'] for x in response['data']['page']['navigation']['navigation'][1]['items']]
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
		endpoint = "https://sports.bovada.lv/rugby-union?json=true"

	elif action == "baseball_matches":
		endpoint = "https://sports.bovada.lv/baseball?json=true"
	
	else:
		raise BovadaException("did not receive a valid action. Received: {}".format(action))
	return endpoint