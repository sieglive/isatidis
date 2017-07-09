# coding:utf-8
"""Predefination of mongo schema."""

import time
from pymongo import MongoClient

from config import CFG as config

M_CLIENT = MongoClient(config.mongo.client).__getattr__(config.mongo.db)

USER_CONTACT = M_CLIENT.user_contact
USER_CONTACT.create_index('user_id', unique=True)
SIGNFLOW_STATUS = M_CLIENT.signflow_status
SIGNFLOW_STATUS.create_index('flow_id', unique=True)
SIGNFLOW_STATUS.create_index('update_time')
SIGNFLOW_STATUS.create_index('waiting_for')
SIGNFLOW_STATUS.create_index('already_signed')


class Clients(object):
    """Class to manage clients of mongo DB."""

    def __init__(self, params):
        self.clients = dict()
        if isinstance(params, list):
            for schema in params:
                self.clients[schema] = M_CLIENT.__getattr__(schema)
        else:
            raise TypeError(
                f"Arguments data should be a 'list' not {type(params)}.")

    def __getattr__(self, name):
        attr = self.clients.get(name)
        if attr is None:
            raise KeyError(name)
        else:
            return attr

    def __getitem__(self, name):
        attr = self.clients.get(name)
        if attr is None:
            raise KeyError(name)
        else:
            return attr


class Tasks:
    """Manager class of tasks."""

    def __init__(self, params):
        if isinstance(params, dict):
            self.tasks = params
        else:
            raise TypeError(
                f"Arguments data should be a 'dict' not {type(params)}.")

    def __getattr__(self, task_name):
        task = self.tasks.get(task_name)
        if task is None:
            raise KeyError(task_name)
        else:
            return task

    def __iter__(self):
        for i in self.tasks:
            yield i

    def __getitem__(self, name):
        task = self.tasks.get(name)
        if task is None:
            raise KeyError(name)
        else:
            return task

    def as_dict(self):
        """Return the task dictonary."""
        return self.tasks


CLIENTS = Clients([
    'login_record', 'logout_record', 'verify_email_record',
    'verify_email_check_record', 'signflow_status', 'payment_record'
])


def insert_login_record(email, user_ip):
    """insert a login record of login action."""
    result = CLIENTS.login_record.insert_one(
        dict(
            email=email,
            user_id=-1,
            login_result='FAILURE',
            login_time=int(time.time()),
            user_ip=user_ip))
    return result.inserted_id


def update_login_record(mid, params):
    """update a login record of specified mid."""
    return CLIENTS.login_record.update_one(dict(_id=mid), {'$set': params})


# class EmailRecord(BASE):
#     """Email record model"""
#     __tablename__ = 'email_record'

#     email_id = Column(CHAR(36), primary_key=True)
#     sender = Column(CHAR(36), nullable=False, index=True)
#     sender_email = Column(String(255), nullable=False, index=True)
#     receiver = Column(CHAR(36), nullable=False, index=True)
#     receiver_email = Column(String(255), nullable=False, index=True)
#     subject = Column(String(255), nullable=False)
#     message = Column(Text, nullable=False)
#     time = Column(Integer, nullable=False, index=True)

MONGO_TOOLS = Tasks(
    dict(
        insert_login_record=insert_login_record,
        update_login_record=update_login_record))
