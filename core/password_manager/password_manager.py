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
from core.Table_Instances.tables import User
from sqlalchemy.orm import sessionmaker
from core.DataEncryption.pass_encrypt import hasher, verify_pass
from sqlalchemy import create_engine, text
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
			print_table(query, User)
		except Exception as VM:
			print(f"<get_user_data> Error: {Fore.LIGHTRED_EX}{str(VM).splitlines()}{Fore.RESET}")



