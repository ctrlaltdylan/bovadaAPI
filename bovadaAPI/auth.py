from error import BovadaException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from .decorators import bovada_api
import time


@bovada_api
def login_to_bovada(driver, *args, **kwargs):
	login_button = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(
			(By.ID, "header-login-button")
			)
		)
	login_button.click()
	username_input = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(
			(By.ID, "login-username")
			)
		)
	password_input = driver.find_element_by_id("login-password")
	username_input.click()
	username_input.send_keys(settings.BOVADA_USERNAME)
	password_input.click()
	password_input.send_keys(settings.BOVADA_PASSWORD)
	submit_button = driver.find_element_by_id("login-submit")
	submit_button.click()
	try:
		error_message = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located(
				(By.ID, 'loginForm-error-message'))
		)
	except:
		login_successful = True

	else:
		login_successful = False
		raise BovadaAuthenticationError(error_message.text)

	if login_successful:
		return True
	return driver
	

