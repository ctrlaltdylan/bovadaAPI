from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
import json


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


def parse_special_response(response):
	return response

def parse_response(response):
	bmatches = []
	center_content = response['data']['regions']['content_center'] #useful
	try:
		gamelines = search_dictionary_for_certain_keys("items", center_content)[0] #index 0 is gamelines index 1 is futures
	except IndexError, TypeError:
		return 
	for match in gamelines['itemList']['items']:
		outcome_objects_for_match = []
		game_sport = match['sport']
		game_id = int(match['id'])
		description = match['description']
		startTime = match['startTime']
		competitors = match['competitors']
		home_team_abbreviation = search_dictionary_for_certain_keys("abbreviation", competitors[1])
		home_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[1])
		home_team_full_name = search_dictionary_for_certain_keys("description", competitors[1])
		away_team_short_name = search_dictionary_for_certain_keys("shortName", competitors[0])
		away_team_abbreviation=  search_dictionary_for_certain_keys("abbreviation", competitors[0])
		away_team_full_name = search_dictionary_for_certain_keys("description", competitors[0])
		game_link = "https://sports.bovada.lv{}".format(match['link'])
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
		
		bmatches.append(bmatch)
		
	return bmatches

def save_bovada_matches(bmatches):
	with open("bmatches.json", "w+") as outfile:
		json.dumps(bmatches, outfile)
			
