import secrets
import string
from typing import Dict, Type, Union, List
from sqlalchemy.ext.declarative import declarative_base as Base
from tabulate import tabulate
from colorama import Fore, Back, Style
from core.DataEncryption.pass_encrypt import verify_pass
from core.Table_Instances.tables import User
import re
import pandas as pd


def authenticate(queried_user: [User], username, passw) -> bool:
	if username == queried_user.Username:
		if verify_pass(queried_user.HashedPassword, passw):
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


def print_table(query: Union[Type[Type], List[Type[Type]]], table_name: Base):
	table_data = []
	if isinstance(query, List):
		for row in query:
			row_data = [getattr(row, column.name) for column in table_name.__table__.columns]
			table_data.append(row_data)
	elif isinstance(query, table_name):
		table_data.append([getattr(query, column.name) for column in table_name.__table__.columns])

	print(tabulate(table_data, headers=table_name.__table__.columns.keys(), tablefmt='sql'))


def generate_salt(length=16):
	"""Generate a cryptographically secure random salt."""
	alphabet = string.ascii_letters + string.digits + string.punctuation
	return ''.join(secrets.choice(alphabet) for i in range(length))


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


def email_checks(email: str):
	regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
	if not re.match(regex, email):
		raise ValueError(f"{Fore.LIGHTRED_EX} Invalid Email syntax provided. {Fore.RESET}")
	domain = email.split('@')[1]
	# if not validate_email(email, verify=True):
	# 	raise ValueError(f"{Fore.LIGHTRED_EX} Provide a valid email{Fore.RESET}")
	return True
