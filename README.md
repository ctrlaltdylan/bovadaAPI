# bovadaAPI
Interact with bovada.lv programmatically.


INSTALLATION:
The easiest way to install is by cloning this repo.

git clone https://github.com/jkol36/bovadaAPI.git

Then: cd bovadaAPI
then: pip install -r requirements.txt
then: add BOVADA_USERNAME and BOVADA_PASSWORD as a environment variable by running export BOVADA_USERNAME="test" export BOVADA_PASSWORD="test"
then: import the bovadaAPI
from bovadaAPI.api import BovadaApi

instantiate the api: b = BovadaApi()
authenticate yourself: b.authenticate


CURRENT_FUNCTIONALITY:
BovadaApi.summary # returns a bunch of information regarding your bovada account
BovadaApi.balance # returns the current amount of money in your bovada account
BovadaApi.open_bets # returns your open bets
BovadaApi.soccer_matches # returns all soccer matches
BovadaApi.basketball_matches # returns all basketball_matches
BovadaApi.rugby_matches # returns all rugby_matches
BovadaApi.tennis_matches # returns all tennis_matches

  




