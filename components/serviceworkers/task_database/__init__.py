# coding:utf-8
"""Query Task of Database esign_v2."""
from workers import Tasks
from workers.task_database.account import TASK_DICT as account_dict
from workers.task_database.file import TASK_DICT as file_dict
from workers.task_database.signflow import TASK_DICT as flow_dict
from workers.task_database.flower import TASK_DICT as flower_dict
from workers.task_database.position import TASK_DICT as position_dict
from workers.task_database.flowrecord import TASK_DICT as flow_record_dict
from workers.task_database.sign import TASK_DICT as sign_dict

TASK_DICT = dict()
TASK_DICT.update(account_dict)
TASK_DICT.update(file_dict)
TASK_DICT.update(flow_dict)
TASK_DICT.update(flower_dict)
TASK_DICT.update(position_dict)
TASK_DICT.update(flow_record_dict)
TASK_DICT.update(sign_dict)

TASKS = Tasks(TASK_DICT)
