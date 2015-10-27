from django.conf import settings
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
	help = "sets your bovada username and password"

	

	def handle(self, *args, **kwargs):
		username = raw_input("bovada_username: ")
		password = raw_input("bovada_password: ")
		if not username and password:
			raise Exception("You forgot to enter either a username or password")
		env = environ.Env(BOVADA_USERNAME=(str, username), 
			BOVADA_PASSWORD=(str, password))

		
