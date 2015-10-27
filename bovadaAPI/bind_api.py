from .error import BovadaException
from decorators import bovada_api
from BovadaBalance import Balance
from BovadaMatches import SoccerMatches, BasketballMatches, BaseballMatches, TennisMatches, RugbyMatches, 





@bovada_api
def bind_api(action=None):
	if action == "balance":
		pass

	elif action == "soccer_matches":
		pass

	elif action == "basketball_matches":
		pass

	elif action == "tennis_matches":
		pass

	elif action == "rugby_matches":
		pass

	elif action == "baseball_matches":
		pass

	else:
		raise BovadaException("got an invalid action as argument")

