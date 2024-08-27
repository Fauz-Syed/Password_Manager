import os
import secrets
import string
import time
from pathlib import Path
import argon2
import argon2.exceptions
from sqlalchemy.dialects.mysql import pymysql
from colorama import Fore, Back, Style

from common.configs.config_file import file
from core.password_manager.helper_funcs import *
import sqlalchemy
from core.Table_Instances.tables import *
from sqlalchemy.orm import sessionmaker
from core.DataEncryption.pass_encrypt import hasher, verify_pass
from sqlalchemy import create_engine, text
from typing import Dict
import pandas as pd
import yaml
from tabulate import tabulate


class PasswordManager:

	def __init__(self, config: str):
		with open(config, 'r') as configs:
			self.yml = yaml.safe_load(configs)
		self.__hook = self.connect_to_db()

	def connect_to_db(self):
		def mysql_connection():
			con = self.yml.get('connections')
			user = con.get('user')
			passw = con.get('pass')
			host = con.get('hostname')
			port = con.get('port')
			database = con.get('database')
			if database is None:
				database_uri = f"mysql+pymysql://{user}:{passw}@{host}:{port}"
			else:
				database_uri = f"mysql+pymysql://{user}:{passw}@{host}:{port}/{database}"
			return database_uri

		uri = mysql_connection()
		engine = create_engine(uri)
		Session = sessionmaker(bind=engine)
		return Session()

	def query(self, query: str, op=None):
		if op is None:
			self.__hook.execute(text(query))
		else:
			self.__hook.execute()
		self.__hook.commit()

	def truncate_data(self, table):
		sql = text(f"DELETE FROM {table}")
		self.__hook.execute(sql)
		self.__hook.commit()
		print("Table truncated")

	def get_all_tables(self):
		return self.yml.get('schemas')

	def insert_users_data(self, Username: str, password: str, Email: str):
		salt = generate_salt(length=20)
		hashpass = salt + password
		new_user = User(Username=Username, HashedPassword=hasher(hashpass), Email=Email, Salt=salt)
		try:
			self.__hook.add(new_user)
			self.__hook.commit()
			print(f"{Fore.GREEN}Account successfully created: {new_user.Username}{Fore.RESET}")
		except sqlalchemy.exc.IntegrityError as ie:
			self.__hook.rollback()
			error = str(ie)
			print(f"<Insert_user_Data> Error:{Fore.LIGHTRED_EX}{error.splitlines()[0]}{Fore.RESET}")
			return False
		return True

	def duplicate_check(self, username: str, email: str):
		df = self._get_all_users()
		if email in df['Email'].values:
			return True
		if username in df['Username'].values:
			return True
		return False

	def get_user_data(self, username, passw):
		# query = self.__hook.query(User).filter_by(Username=username).first()
		query = text(f"SELECT * FROM users WHERE Username= :username")
		stmt = self.__hook.execute(query, {'username': username})
		df = pd.DataFrame(stmt.fetchall())
		try:
			passw = df['Salt'].item() + passw
			if authenticate(df, username, passw):
				print(f"{Fore.GREEN}Authenticated Successfully: {username}{Style.RESET_ALL}")
				return df
		except Exception as VM:
			print(f"<get_user_data> Error: {Fore.LIGHTRED_EX}{str(VM).splitlines()}{Fore.RESET}")
		return False

	def log_in(self, username, passw, show_data="do not"):
		if username == "  ":
			return None
		result = self.get_user_data(username, passw)
		if result is False:
			raise Exception(f"<log_in> error logging in")
		if show_data == "show":
			print(f"{Fore.BLUE}Welcome {username}, to the Password Manager homepage.{Fore.RESET}")
			time.sleep(1)
			print_table(result[["UserID", "Username", "CreatedAt"]])

		return result

	"""
	Insert_password is desigend to take user input and create it into a config dictionary. 
	"""

	def insert_password_entry(self, passw_config: Dict[str, str]):
		inserted = False
		if passw_config is not None:
			query = text(f"Insert into passwordentries (UserID, Website, Web_Username, EncryptedPassword, Note) "
						 f"Values (:UserID, :website, :web_username, :web_password, :desc)")
			stmt = self.__hook.execute(query, passw_config)
			self.__hook.commit()
			print(f"{Fore.GREEN}Password successfully inserted for:\nwebsite - {passw_config['website']}\nweb_user - "
				  f"{passw_config['web_username']} {Fore.RESET}")

	def print_user_passwords(self, UserID):
		print("PM print: ", UserID, "\n--------------------------------------------")
		query = text(
			f"SELECT users.Username, Website, Web_Username, EncryptedPassword From users join passwordentries pe on users.UserID = pe.UserID Where users.UserID = :UserID;")
		stmt = self.__hook.execute(query, {'UserID': UserID})
		pass_df = pd.DataFrame(stmt.fetchall())
		print_table(pass_df)

	def print_specifc_passwords(self, UserID, spec_web):
		query = text(
			"SELECT users.Username, Website, Web_Username, EncryptedPassword FROM users JOIN passwordentries pe ON "
			"users.UserID = pe.UserID WHERE Website = :spec_web and users.UserID = :UserID;")
		stmt = self.__hook.execute(query, {"UserID": UserID, "spec_web": spec_web})
		pass_df = pd.DataFrame(stmt.fetchall())
		print_table(pass_df)

	def _get_all_users(self):
		query = text("SELECT * FROM users;")
		stmt = self.__hook.execute(query)
		return pd.DataFrame(stmt.fetchall())

	def email_search(self, email):
		query = text("SELECT * FROM users WHERE Email = :email;")
		stmt = self.__hook.execute(query, {"email": email})
		return pd.DataFrame(stmt.fetchall())


pm = PasswordManager(file)

