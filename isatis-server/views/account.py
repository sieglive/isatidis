# coding: utf-8
"""Account Views' Module"""

import json
import time
from tornado.web import asynchronous
from tornado.gen import coroutine, sleep
from views import BaseHandler


class SignIn(BaseHandler):
    """Handle Login Request."""

    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        email = self.get_argument('email')
        pswd = self.get_argument('password')
        args = dict(email=email, password=pswd, time=time.time())
        self.finish(json.dumps(args))


class SignUp(BaseHandler):
    """Handle LogOn Request."""
    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_args(['email', 'password'])
        args.add('msg', 'params accessed.')
        self.finish(json.dumps(args.to_dict()))


ACCOUNT_URL = [
    (r'/middle/account/signin', SignIn),
    (r'/middle/account/signup', SignUp),
]
