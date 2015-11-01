def was_successful(request):
	if request.status_code == 200:
		return True
	else:
		return False
