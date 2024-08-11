from typing import Dict

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
	__tablename__ = 'Users'
	UserID = Column(Integer, primary_key=True, autoincrement=True)
	Username = Column(String(255), nullable=False, unique=True)
	Email = Column(String(255), nullable=False, unique=True)
	HashedPassword = Column(String(1000), nullable=False)
	Salt = Column(String(255), nullable=False)
	CreatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
	UpdatedAt = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(),
					   nullable=False)
	columns_to_display = ['UserID', 'Username', 'HashedPassword', 'Email', 'Salt']
