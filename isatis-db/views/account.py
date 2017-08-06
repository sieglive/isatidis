# coding: utf-8
"""Account Views' Module"""

import time
from uuid import uuid1 as uuid
from tornado.web import asynchronous
from tornado.gen import coroutine
from views import BaseHandler

from workers import TASKS as tasks


class Account(BaseHandler):

    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_arguments(
            ['user_pass', 'email'])
        print(args.args)

    @asynchronous
    @coroutine
    def put(self, *_args, **_kwargs):
        args = self.parse_json_arguments(
            ['user_name', 'nick_name', 'user_pass', 'email'])
        print(args.args)
        result = yield self.waiting_result(
            tasks.insert_account,
            kwargs=dict(
                user_name=args.user_name,
                nick_name=args.nick_name,
                user_pass=args.user_pass,
                email=args.email,
                appear_time=int(time.time()),
                register_time=int(time.time()),))


ACCOUNT_URL = [
    (r'/back/account/auth', Account)
]
