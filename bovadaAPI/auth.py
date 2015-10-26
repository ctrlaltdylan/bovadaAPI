from error import BovadaException

def login_to_bovada(session, username, password):
	print "logging into bovada"
	if not username:
		raise BovadaException("you forgot to supply a username")
	if not password:
		raise BovadaException("you forgot to supply a password")

	page, resources = session.evaluate("document.getElementById('header-login-button').click()", expect_loading=True)
	

