import secrets
import string
from typing import Dict, Type
from core.password_manager.password_manager import PasswordManager
from core.DataEncryption.pass_encrypt import verify_pass
from core.Table_Instances.tables import User
import pandas as pd

session = PasswordManager.connect_to_db("password_manager")


def authenticate(queried_user: [User], username, passw) -> bool:
	if username == queried_user.Username:
		if verify_pass(queried_user.HashedPassword, passw):
			return True
		else:
			print('Wrong password')
	else:
		print("Wrong username")


def print_query_table(table_config: Dict[str, Type], table):
	get = session.query(table).all()
	data = User.create_tables(get)
	pd.set_option('display.max_columns', None)  # Show all columns
	pd.set_option('display.expand_frame_repr', False)  # Prevent line wrapping
	df = pd.DataFrame(data)
	print(df)


def generate_salt(length=16):
	"""Generate a cryptographically secure random salt."""
	alphabet = string.ascii_letters + string.digits + string.punctuation
	return ''.join(secrets.choice(alphabet) for i in range(length))
