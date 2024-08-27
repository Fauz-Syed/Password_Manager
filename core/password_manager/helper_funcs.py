import re
import secrets
import string
import time
from typing import Union
import core.password_manager.password_manager as pm
import pandas as pd
from colorama import Fore, Style
from sqlalchemy import Result
from tabulate import tabulate

from common.configs.config_file import file
from core.DataEncryption.pass_encrypt import verify_pass


def authenticate(queried_user: pd.DataFrame, username, passw) -> bool:
	if username == queried_user['Username'].item():
		print(f"{Fore.GREEN}Username {username} is a match {Fore.RESET}")
		time.sleep(1)
		if verify_pass(queried_user['HashedPassword'].item(), passw):
			print(f"{Fore.GREEN}Password for {username} is a match {Fore.RESET}")
			return True
		else:
			print('Wrong password')
	else:
		print("Wrong username")


"""
The print table works in two different ways: Type[Base] and List[Type[Base]]. In the Example we will use the class User 
which is th class that defines the table in the ORM way of using SQLAlchemy.

Union allows for one positional argument to be a possibility of a list of things: Type[User] or List[Type[User]]

Type[User]: the actual class itself and not the instance of the class. A blueprint for an instance.
	- User(UserID, Username, Email, ... )
List[Type[User]]: A list of of different blueprints that are based on the User class
	- [
	   User(UserID, Username, Email, ... ), 
	   User(UserID, Username, Email, ... ), 
	   User(UserID, Username, Email, ...),
	   ...
	   ]


"""


def print_table(stmt: Union[Result, pd.DataFrame] = None, frmt: str = "pretty", color=Fore.LIGHTMAGENTA_EX):
	if isinstance(stmt, Result):
		df = pd.DataFrame(stmt.fetchall(), columns=stmt.keys())
		print(tabulate(df, headers=stmt.keys(), tablefmt=frmt))
	if isinstance(stmt, pd.DataFrame):
		print(f'{color}', tabulate(stmt, headers=stmt.keys(), tablefmt=frmt), f'{Style.RESET_ALL}')


def generate_salt(length=16):
	alphabet = string.ascii_letters + string.digits + string.punctuation
	return ''.join(secrets.choice(alphabet) for _ in range(length))


def username_checks(username: str):
	if len(username) < 6:
		raise ValueError(f"{Fore.LIGHTRED_EX}Username must be at least 6 characters long.{Fore.RESET}")
	characters = [' ', '/', '-']
	if any(char in username for char in characters):
		raise ValueError(f"{Fore.LIGHTRED_EX}Username cannot contain {characters}. {Fore.RESET}")
	return True


def password_checks(password: str, confirm: str):
	if len(password) < 8:
		raise ValueError(f"{Fore.LIGHTRED_EX} Password must be at least 8 characters long.{Fore.RESET}")
	if not any(char.isdigit() for char in password):
		raise ValueError(f"{Fore.LIGHTRED_EX} Password must contain Numbers and special characters.{Fore.RESET}")
	special = string.punctuation
	if not any(char in special for char in password):
		raise ValueError(f"{Fore.RED} Password must contain Numbers and special characters.{Fore.RESET}")
	if password != confirm:
		raise ValueError(f"{Fore.LIGHTRED_EX} Passwords do not match.{Fore.RESET}")
	return True


def email_checks(email: str, username: str):
	regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
	if not re.match(regex, email):
		raise ValueError(f"{Fore.LIGHTRED_EX} Invalid Email syntax provided. {Fore.RESET}")
	domain = email.split('@')[1]
	if pm.PasswordManager(file).duplicate_check(username=username, email=email):
		return False
	# if not validate_email(email, verify=True):
	# 	raise ValueError(f"{Fore.LIGHTRED_EX} Provide a valid email{Fore.RESET}")

	return True
