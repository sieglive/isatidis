# coding:utf-8
"""Module of Celery Tasks"""
from config import CFG as config
from config import _ENV as env
from utils.oss_handler import Oss

from utils.celery_tools import dec2hex
from utils.celery_tools import serial
from utils.celery_tools import bindserial
from utils.celery_tools import spam_encode
from utils.celery_tools import spam_decode
from utils.celery_tools import extract_params
from utils.celery_tools import add_label
from utils.celery_tools import change_ext
from utils.celery_tools import basename

from utils.utils import figure_id, Tasks
