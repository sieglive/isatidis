# coding:utf-8
"""Module of celery task queue manager."""
import traceback
from functools import wraps

from celery import Celery

from . import env, config

APP = Celery(
    'tasks',
    backend=config.converter.celery.backend,
    broker=config.converter.celery.broker, )

APP.conf.update(
    task_serializer='json',
    result_serializer='json',
    result_expires=1800,
    task_default_queue='default',
    task_default_exchange='tasks',
    task_default_exchange_type='topic',
    task_default_routing_key='task.default',
    task_routes={
        'workers.task_serverupload.*': {
            'queue': env + '_serverupload'
        },
    })

