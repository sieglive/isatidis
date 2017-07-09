# coding:utf-8
"""isatis models."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import SmallInteger
from sqlalchemy import CHAR
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Account(BASE):
    """Account Model."""

    __tablename__ = 'isatis_account'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), index=True, unique=True, nullable=False)
    nick_name = Column(String(100))
    user_pass = Column(CHAR(32), nullable=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    permission = Column(SmallInteger, default=0)
    avatar_path = Column(CHAR(255))
    active_status = Column(SmallInteger, default=0)
    valid = Column(SmallInteger, default=1)
    appear_time = Column(Integer, index=True, nullable=False)
    register_time = Column(Integer, index=True, nullable=False)
    expire_time = Column(Integer, index=True, default=0)
