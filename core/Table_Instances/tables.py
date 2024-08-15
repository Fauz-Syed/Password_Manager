from typing import Dict
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class User(Base):
	__tablename__ = 'Users'
	UserID = Column(Integer, primary_key=True, autoincrement=True)
	Username = Column(String(255), primary_key=True, nullable=False, unique=True)
	Email = Column(String(255), nullable=False, unique=True)
	HashedPassword = Column(String(1000), nullable=False)
	Salt = Column(String(255), nullable=False)
	CreatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
	UpdatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
					   nullable=False)

	entries = relationship("PasswordTable", cascade="all, delete, delete-orphan")
	# users = relationship("PasswordTable", cascade="all, delete, delete-orphan")
	columns_to_display = ['UserID', 'Username', 'HashedPassword', 'Email', 'Salt']


class PasswordTable(Base):
	__tablename__ = 'passwordentries'
	EntryID = Column(Integer, primary_key=True, autoincrement=True)
	UserID = Column(Integer, ForeignKey('Users.UserID'))
	Website = Column(String(1000), nullable=False)
	Web_Username = Column(String(255))
	EncryptedPassword = Column(String(1000))
	Note = Column(Text)
	CreatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
	updatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

	columns_to_display = ['UserID', 'Website', 'Web_Username', 'EncryptedPassword', 'Description']
