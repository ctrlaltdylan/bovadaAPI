


def get_bovada_headers_generic():
	headers = {"Accept": "application/json", 
	"Content-Type":"application/json;charset=utf-8", 
	"Connection":"keep-alive", 
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"}
	return headers

def get_bovada_headers_authorization(auth_token, token_type):
	headers = get_bovada_headers_generic()
	headers["Authorization"] = token_type+" "+auth_token
	return headers





def validate_bet_blueprint(outcome, priceId, stake):

	"""
	attributes to change:
		replace_outcome = data["selections"][0]["selection"]["outcomeId"] #the outcome to bet on
		replace_priceId = data["selections"][0]["selection"]["priceId"] #the id of the price (AKA, the odds, payout)
		replace_stake = data["bets"]["bet"][0]["stakePerLine"] #the amount to bet 100 = $1, 1000= $10 10000=$100

	notes:
		selections is a list so naturally you can add additional selection objects, 
		but for now we're just going to get this to work with a single selection object.
	"""
	data = {
		"channel":"WEB_BS",
		"selections":
			{
				"selection":
					[
						{
							"outcomeId":"93276072",
							"id":0,
							"system":"A",
							"priceId":"79887032",
							"oddsFormat":"DECIMAL"
						}
					]
			},
		"groups":
			{	
				"group":
					[
						{
							"type":"STRAIGHT",
							"groupSelections":
								[
									{
										"groupSelection":
										[
											{
												"selectionId":0,
												"order":0
											}
										]
									}
								],
							"id":0
						}
					]
			},
		"bets":
			{
				"bet":
					[
						{
							"betType":"SINGLE",
							"betGroups":
								{
									"groupId":[0]
								},
								"stakePerLine":100,
								"isBox":False,
								"oddsFormat":"DECIMAL",
								"specifyingRisk":True
						}
					]
			}
	}

	replace_outcome = data["selections"][0]["selection"]["outcomeId"] #the outcome to bet on
	replace_priceId = data["selections"][0]["selection"]["priceId"] #the id of the price (AKA, the odds, payout)
	replace_stake = data["bets"]["bet"][0]["stakePerLine"] #the amount to bet 100 = $1, 1000= $10 10000=$100
