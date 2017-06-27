# coding: utf-8
"""Account Views' Module"""

import json
from tornado.web import asynchronous
from tornado.gen import coroutine
from views import BaseHandler


class Login(BaseHandler):
    """Handle Login Request."""
    @asynchronous
    @coroutine
    def post(self, *_args, **_kwargs):
        args = self.parse_json_args(['email', 'password'])
        args.add('msg', 'params accessed.')
        self.finish(json.dumps(args.to_dict()))


ACCOUNT_URL = [
    (r'/account/login', Login),
]
