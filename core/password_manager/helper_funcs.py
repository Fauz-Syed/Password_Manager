import secrets
import string
from typing import Dict, Type, Union, List
from sqlalchemy.ext.declarative import declarative_base as Base
from tabulate import tabulate

from core.DataEncryption.pass_encrypt import verify_pass
from core.Table_Instances.tables import User
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
