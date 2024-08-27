import sys
import time

import keyboard
import pandas as pd
from sqlalchemy import text

import core.password_manager.password_manager as pm
from core.password_manager.helper_funcs import username_checks, password_checks, email_checks, print_table
from core.DataEncryption.pass_encrypt import hasher, verify_pass
import os
from colorama import Fore, Back, Style
from common.configs.config_file import file

# table = ["users"]


# test = pm.PasswordManager(file, "password_manager")
# test.truncate_data(table)
# test.insert_users_data(Username="zainub", password="hello!", Email="zgirl@gmail.com")
# test.insert_users_data(Username="t", password="sbfz2009!", Email="bin@gmail.com")
# test.get_user_data("zainub", "hello!")

manager = pm.PasswordManager(file)


def create_new_user():
	cycle = True
	username = ""
	password = ""
	email = ""
	a, b, c = False, False, False
	print(f"{Fore.YELLOW}Creating new User{Style.RESET_ALL}")
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
				if not email_checks(username=username, email=email):
					print(f"<create_new_user> An error occurred: Duplicate email or Username")
					a = False
					c = False
				else:
					c = True
			except Exception as e:
				print(f"<create_new_user>An error occurred: {e.with_traceback(e.__traceback__)}")

		except Exception as e:
			pass

		if a is True and b is True and c is True:
			try:
				if manager.insert_users_data(username, password, email):
					cycle = False
			except Exception as e:
				print(f"<create_new_user> An error occurred: {e}")


def add_passw(df: pd.DataFrame):
	passw = {
		"UserID": df['UserID'].item(),
		"website": input("Enter the website you would like to save password for: "),
		"web_username": input("Enter your username: "),
		"web_password": input("Enter your password: "),
		"desc": input("enter your description: ")
	}
	manager.insert_password_entry(passw)


def log_in_func():
	username = input("Enter your username: ")
	password = input("Enter your password: ")
	show_data = input("Do you want to show data? do not or show: ")
	return manager.log_in(username, password, show_data)


def spinner_log_off():
	spinner = ['|', '/', '-', '\\']
	print("Logging off ", end="")
	sys.stdout.flush()  # Ensures the text is displayed immediately

	for _ in range(10):  # Spin for a certain number of cycles
		for symbol in spinner:
			sys.stdout.write(symbol)
			sys.stdout.flush()
			time.sleep(0.1)  # Pause for a short moment to create the spinning effect
			sys.stdout.write('\b')  # Backspace to overwrite the previous symbol

	print("\nLogged off successfully!")


def display_user_passwords(df: pd.DataFrame):
	manager.print_user_passwords(df['UserID'].item())


def specific_web_passes(df: pd.DataFrame):
	manager.print_specifc_passwords(df['UserID'].item(), spec_web=input("Website Search: "))


def delete_table():
	manager.truncate_data("users")
