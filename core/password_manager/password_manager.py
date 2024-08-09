import os
import secrets
import string
from pathlib import Path

import argon2.exceptions

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

	def __init__(self, config: str, database=None):
		with open(config, 'r') as configs:
			self.yml = yaml.safe_load(configs)
		self.hook = self.connect_to_db(database)

	def connect_to_db(self, database: str):
		def mysql_connection(database: str):
			con = self.yml.get('connections')
			user = con.get('user')
			passw = con.get('pass')
			host = con.get('hostname')
			port = con.get('port')
			if database is None:
				database_uri = f"mysql+pymysql://{user}:{passw}@{host}:{port}"
			else:
				database_uri = f"mysql+pymysql://{user}:{passw}@{host}:{port}/{database}"
			return database_uri

		uri = mysql_connection(database)
		engine = create_engine(uri)
		Session = sessionmaker(bind=engine)
		return Session()

	def query(self, query: str, op=None):
		if op is None:
			self.hook.execute(text(query))
		else:
			self.hook.execute()
		self.hook.commit()

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
			self.hook.add(new_user)
			self.hook.commit()
		except sqlalchemy.exc.IntegrityError as ie:
			self.hook.rollback()
			print("User already has been added")

	def get_user_data(self, username, passw):
		user = self.hook.query(User).filter_by(Username=username).first()
		passw = user.Salt + passw
		try:
			authenticate(user, username, passw)

		except Exception as VM:
			print(f"{VM}")


t = "C:\\Users\\fauzs\\OneDrive\\Desktop\\Codes\\PyCharm Projects\\Password_manager\\common\\configs\\config.yml"
table = ["users"]
test = PasswordManager(t, "password_manager")
# test.truncate_data(table)
test.insert_users_data(Username="FauzSyed", password="Fireiscool123!", Email="fauz.syed234@gmail.com")
test.get_user_data("FauzSyed", "Fireiscool123!")
