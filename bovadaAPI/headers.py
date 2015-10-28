


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