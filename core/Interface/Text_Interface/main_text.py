import sys

import pandas as pd

from text_interface import *


def start_app():
	result = None
	active = True
	logged_in = False
	counter = 0
	user = pd.DataFrame()
	while active:
		if not logged_in:
			action = str(input("log off (0) : create new user (1) : log in (2)\n"))
			if action == "1":
				create_new_user()
			if action == "2":
				t = True
				while t:
					try:
						result = log_in_func()
						t = False
					except Exception as e:
						pass
				if result is None:
					logged_in = False
				else:
					logged_in = True
			if action == "0":
				spinner_log_off()
				break
		elif logged_in:
			action = str(
				input("would you like to | (0) sign off | (1) display your passwords | "
					  "(2) add a password | (3) show specific website password |\n"))
			if action == "1":
				display_user_passwords(result)
			if action == "2":
				add_passw(result)
			if action == "0":
				logged_in = False
			if action == "3":
				specific_web_passes(result)
			if action == "delete":
				if result['isAdmin'].item() != 1:
					print("You are not allowed to delete tables")
				else:
					deletion = input("Confirm deletion of all data? Y or N")
					if deletion == "Y":
						delete_table()


start_app()
