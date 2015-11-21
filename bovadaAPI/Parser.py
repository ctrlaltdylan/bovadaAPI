from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys
import json
from error import BovadaException


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

	@classmethod
	def create_from_center_content(cls, content_center):
		match = search_dictionary_for_certain_keys("items", content_center)[0]
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
					outcomes = OutCome.create_from_betting_line(line)
					for outcome in outcomes:
						outcome_objects_for_match.append(outcome)


					

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
		return bmatch
	@classmethod
	def bulk_create_from_center_content(cls, center_content):
		bmatches = []
		try:
			gamelines = search_dictionary_for_certain_keys("items", center_content)[0] #index 0 is gamelines index 1 is futures
		except (IndexError, TypeError):
			return []
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
						outcomes = OutCome.create_from_betting_line(line)
						for outcome in outcomes:
							outcome_objects_for_match.append(outcome)


						

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


class OutCome(object):
	def __init__(self, *args, **kwargs):
		#if odds_type == Totals we will have a total amount
		#if odds_type == Point Spread we will have a spread amount
		#the price is the odds
		self.odds_type = kwargs.pop("odds_type")
		self.name = kwargs.pop("name")
		try:
			self.total_amount = kwargs.pop("total_amount")
		except:
			self.total_amount = None
		try:
			self.spread_amount = kwargs.pop("spread_amount")
		except:
			self.spread_amount = None
		self.price = kwargs.pop("price")
		self.price_id = kwargs.pop("price_id")
		self.outcome_id = kwargs.pop("outcome_id")
		return super(OutCome, self).__init__()

	@classmethod
	def create_from_betting_line(cls, betting_line, *args, **kwargs):
		outcome_objs = []
		#each odds_type has it's own outcome objects
		odds_type = betting_line["description"]
		outcomes = betting_line["outcomes"]

		for outcome in outcomes:
			spread_amount = None
			total_amount = None
			
			if odds_type == "Total":
				try:
					total_amount = float(outcome["price"]["handicap"])
				except:
					pass
			if odds_type == "Point Spread" or odds_type == "Goal Spread" or odds_type=="Point Spread - Sets":
				try:
					spread_amount = float(outcome["price"]["handicap"])
				except:
					pass
	
			
			try:
				name = outcome["description"]
			except KeyError, e:
				name = None
			try:
				price = float(outcome["price"]['decimal'])
			except KeyError, e:
				price = None

			try:
				status = outcome['status']
			except KeyError, e:
				status = None
			try:
				price_id = int(outcome['price']['id'])
			except KeyError, e:
				price_id = None
			try:
				outcome_id = int(outcome['price']['outcomeId'])
			except KeyError, e:
				outcome_id = None

			if status == "OPEN":
				outcome_objs.append(
					cls(
						odds_type=odds_type,
						name=name,
						price=price,
						price_id=price_id,
						spread_amount=spread_amount,
						total_amount=total_amount,
						outcome_id=outcome_id
					)
				)
		return outcome_objs




def parse_special_response(response, action):
	if action == "balance":
		return int(search_dictionary_for_certain_keys("availableBalance", response.json())["amount"])
	return response

def parse_response(response):
	center_content = response['data']['regions']['content_center'] #useful
	bmatches = BovadaMatch.bulk_create_from_center_content(center_content)
	return bmatches

	

def save_bovada_matches(bmatches):
	with open("bmatches.json", "w+") as outfile:
		json.dumps(bmatches, outfile)
			
