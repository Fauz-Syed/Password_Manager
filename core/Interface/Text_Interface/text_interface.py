import core.password_manager.password_manager as pm
from core.password_manager.helper_funcs import username_checks, password_checks, email_checks
import os
from colorama import Fore, Back, Style

# table = ["users"]
file = "C:\\Users\\fauzs\\OneDrive\\Desktop\\Codes\\Projects 2024\\Password_Manager\\common\\configs\\config.yml"


# test = pm.PasswordManager(file, "password_manager")
# test.truncate_data(table)
# test.insert_users_data(Username="zainub", password="hello!", Email="zgirl@gmail.com")
# test.insert_users_data(Username="t", password="sbfz2009!", Email="bin@gmail.com")
# test.get_user_data("zainub", "hello!")


def create_new_user():
	cycle = True
	username = ""
	password = ""
	email = ""
	a, b, c = False, False, False
	while cycle:
		if a is False:
			username = input("Enter your username: ")
		if b is False:
			password = input("Enter your password: ")
			confirm_password = input("confirm your password: ")
		if c is False:
			email = input("Enter your email: ")
		try:
			try:
				a = username_checks(username)
			except Exception as e:
				print(f"<create_new_user> An error occurred: {e}")

			try:
				b = password_checks(password, confirm_password)
			except Exception as e:
				print(f"<create_new_user> An error occurred: {e}")

			try:
				c = email_checks(email)
			except Exception as e:
				print(f"<create_new_user>An error occurred: {e}")

		except Exception as e:
			pass

		if a is True and b is True and c is True:
			try:
				manager = pm.PasswordManager(file)
				if manager.insert_users_data(username, password, email):
					cycle = False
			except Exception as e:
				print(f"<create_new_user> An error occurred: {e}")


create_new_user()
