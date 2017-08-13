# coding: utf-8
"""Account Views' Module"""

import json
import time
from hashlib import md5
from uuid import uuid1 as uuid
from tornado.web import asynchronous
from tornado.gen import coroutine, sleep
from views import BaseHandler


class SignIn(BaseHandler):
    """Handle Login Request."""

    @asynchronous
    @coroutine
    def get(self, *_args, **_kwargs):
        res = self.check_auth(2)
        if not res:
            return
        else:
            _user_id, _params = res

        res = dict(
            result=1,
            status=0,
            data=_params,
            msg='Log in successfully.')
        self.finish_with_json(res)

    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_arguments(['email', 'password'])
        account_info = self.user_account.find_one({'email': args.email})
        if not account_info:
            return self.dump_fail_data(3001)
        if md5(args.password.encode()).hexdigest() != account_info['password']:
            return self.dump_fail_data(3001)

        self.set_current_user(account_info.get('user_id'))
        self.set_parameters(account_info.get('info'))
        res = dict(
            result=1,
            status=0,
            data=account_info.get('info'),
            msg='Log in successfully.')
        self.finish_with_json(res)


class SignUp(BaseHandler):
    """Handle LogOn Request."""

    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_arguments(['nickname', 'email', 'password'])
        user_exists = self.user_account.find_one(dict(email=args.email))

        if user_exists:
            return self.dump_fail_data(3004)
        user_id = str(uuid())
        self.user_account.update_one(
            {'email': args.email},
            {'$set': {
                'user_id': user_id,
                'email': args.email,
                'info': {
                    'nickname': args.nickname,
                    'email': args.email,
                    'user_id': user_id
                },
                'password': md5(args.password.encode()).hexdigest()
            }},
            upsert=True)
        res = dict(
            result=1,
            status=0,
            data=None,
            msg='Sign up successfully.')
        self.finish_with_json(res)


ACCOUNT_URL = [
    (r'/middle/account/signin', SignIn),
    (r'/middle/account/signup', SignUp),
]
