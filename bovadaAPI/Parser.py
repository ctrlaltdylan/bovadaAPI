

all_bmatches = []



def parse_special_response(response):
	return response

def parse_response(response):
	bmatches = []
	center_content = response['data']['regions']['content_center'] #useful
	market_lines =  search_dictionary_for_certain_keys("value", [value for value in response['data']['regions']['content_center'].values()][0])#other keys = name, value#returns odds ['json-var']['value']
	try:
		gamelines = search_dictionary_for_certain_keys("items", center_content)[0] #index 0 is gamelines index 1 is futures
	except IndexError:
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
		all_bmatches.append(bmatch)
	return all_bmatches
			
