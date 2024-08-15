import os
import secrets
import string
from pathlib import Path
import argon2
import argon2.exceptions
from sqlalchemy.dialects.mysql import pymysql
from colorama import Fore, Back, Style
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

	def truncate_data(self, tables):
		for table in tables:
			sql = f"TRUNCATE TABLE {table}"
			self.query(sql)

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

	def get_user_data(self, username, passw):
		query = self.__hook.query(User).filter_by(Username=username).first()
		try:
			passw = query.Salt + passw
			authenticate(query, username, passw)
			return query, True
		except Exception as VM:
			print(f"<get_user_data> Error: {Fore.LIGHTRED_EX}{str(VM).splitlines()}{Fore.RESET}")
		return None, False

	"""
	Insert_password is desigend to take user input and create it into a config dictionary. 
	"""
	def insert_password_entry(self, passw: Dict[str, str], user: Type[User]):

		if passw is not None:
			web_username = passw['web_username']
			web_password = passw['web_password']
			website = passw['website']
			desc = passw['desc']
			new_password = PasswordTable(Website=website, Web_Username=web_username, EncryptedPassword=web_password, Note=desc)
			user.entries.append(new_password)
			self.__hook.commit()
			print(f"{Fore.GREEN} Password successfully inserted for:\n website - {website}\nweb_user - {web_username} {Fore.RESET}")
		query = self.__hook.query(PasswordTable.EntryID, User.Username, PasswordTable.Website, PasswordTable.Web_Username).join(PasswordTable).all()
		print_table(query=query, header=["Username", "Website", "Web_Username"])


# file = "C:\\Users\\fauzs\\OneDrive\\Desktop\\Codes\\Projects 2024\\Password_Manager\\common\\configs\\config.yml"
#
# test = PasswordManager(file)
# test.truncate_data(table)
# test.insert_users_data(Username="zainub", password="hello!", Email="zgirl@gmail.com")
# test.insert_users_data(Username="t", password="sbfz2009!", Email="bin@gmail.com")
# test.get_user_data("zainub", "hello!")
