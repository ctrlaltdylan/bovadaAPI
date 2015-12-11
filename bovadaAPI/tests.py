import unittest
import itertools
from api import BovadaApi
b = BovadaApi()
auth_obj = b.auth



def createBovadaBasketBallMatches():
	return b.basketball_matches

def createBovadaSoccerMatches():
	return b.soccer_matches

def createBovadaTennisMatches():
	return b.tennis_matches

def createBovadaRugbyMatches():
	return b.rugby_matches

def createBovadaBaseBallMatches():
	return b.baseball_matches

def createFootBallMatches():
	return b.football_matches





class MyTest(unittest.TestCase):
	#passed
	def testRugbyMatchesCreate(self):
		return createBovadaRugbyMatches()
	def findNullAttributesOfBovadaMatch(self):
		exclude_endpoints = []
		all_matches = itertools.chain(
			createBovadaRugbyMatches(),
			createFootBallMatches(),
			createBovadaSoccerMatches(),
			createBovadaTennisMatches(),
			createBovadaBaseBallMatches(),
			createBovadaBasketBallMatches())
		for match in all_matches:
			printed_link = False
			for key, value in match.__dict__.iteritems():
				if value is None:
					exclude_endpoints.append(match.game_link)
					print key + "is none"
		print exclude_endpoints

	def assertIsList(self, input):
		return isinstance(input, list)

	def assertCompareOutcomesWorks(self):
		all_matches = itertools.chain(
			createBovadaRugbyMatches(),
			createFootBallMatches(),
			createBovadaSoccerMatches(),
			createBovadaTennisMatches(),
			createBovadaBaseBallMatches(),
			createBovadaBasketBallMatches()
		)

		for match in all_matches:
			for outcome in match.outcomes:
				print "".join(x for x in outcome.odds_type.split(" ")).lower()



	def assertTotalValid(self):
		all_matches = itertools.chain(
			createBovadaRugbyMatches(),
			createFootBallMatches(),
			createBovadaSoccerMatches(),
			createBovadaTennisMatches(),
			createBovadaBaseBallMatches(),
			createBovadaBasketBallMatches()
		)
		for match in all_matches:
			for outcome in match.outcomes:
				if "Total" in outcome.odds_type:
					if (
							outcome.total_amount is not None and
							outcome.odds is not None and 
							outcome.outcome_type is not None
						) == False:
						print outcome.total_amount
						print outcome.odds
						print outcome.outcome_type
				else:
					pass
				 

	def assertMoneyLineValid(self):
		all_matches = itertools.chain(
			createBovadaRugbyMatches(),
			createFootBallMatches(),
			createBovadaSoccerMatches(),
			createBovadaTennisMatches(),
			createBovadaBaseBallMatches(),
			createBovadaBasketBallMatches()
		)
		for match in all_matches:
			for outcome in match.outcomes:
				if "MoneyLine" in outcome.odds_type:
					if (
							outcome.odds is not None and 
							outcome.outcome_type is not None
						) == False:
						print "invalid"
				else:
					pass

	def runTest(self):
		self.assertCompareOutcomesWorks()







t = MyTest()
t.runTest()
