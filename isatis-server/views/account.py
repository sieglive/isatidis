# coding: utf-8
"""Account Views' Module"""

import json
import time
from tornado.web import asynchronous
from tornado.gen import coroutine, sleep
from views import BaseHandler


class Login(BaseHandler):
    """Handle Login Request."""
    @asynchronous
    @coroutine
    def get(self, *_args, **_kwargs):
        email = self.get_argument('email')
        pswd = self.get_argument('password')
        args = dict(email=email, password=pswd, time=time.time())
        yield sleep(2)
        self.finish(json.dumps(args))

    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_args(['email', 'password'])
        args.add('msg', 'params accessed.')
        self.finish(json.dumps(args.to_dict()))


ACCOUNT_URL = [
    (r'/middle/account/login', Login),
]
