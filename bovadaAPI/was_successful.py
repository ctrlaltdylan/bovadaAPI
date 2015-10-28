



def was_successful(request):
	print "calling was_successful"
	if request.status_code == 200:
		return True
	else:
		return request.status_code