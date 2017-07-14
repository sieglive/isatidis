# coding:utf-8
"""Module of Celery Tasks"""
from config import CFG as config
from config import _ENV as env

from workers import Tasks
from workers.manager import APP as app
from workers.task_database.account import TASK_DICT as account_dict

TASK_DICT = dict()
TASK_DICT.update(account_dict)

TASKS = Tasks(TASK_DICT)
