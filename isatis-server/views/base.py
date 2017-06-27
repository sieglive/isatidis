# coding:utf-8
"""Base Module of other View Modules."""

import json
from tornado.web import RequestHandler, MissingArgumentError


class Arguments():
    """Trick dict as a JS object."""

    def __init__(self, args):
        self.args = args

    def __getattr__(self, key):
        if key in self.args:
            if isinstance(self.args[key], dict):
                res = Arguments(self.args[key])
            else:
                res = self.args[key]
        else:
            res = None
        return res

    def __getitem__(self, key):
        if key in self.args:
            if isinstance(self.args[key], dict):
                res = Arguments(self.args[key])
            else:
                res = self.args[key]
        else:
            res = None
        return res

    def to_dict(self):
        return self.args

    def keys(self):
        return self.args.keys()

    def count(self):
        return len(self.args.keys())

    def add(self, key, value):
        self.args[key] = value


class BaseHandler(RequestHandler):
    """Rewrite some method of RequestHandler."""

    def get(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def put(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def post(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def delete(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def head(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def options(self, *_args, **_kwargs):
        self.write('405: Method Not Allowed.')

    def data_received(self, chunk):
        self.write('405: Method Not Allowed.')

    def parse_json_args(self, key_list):
        try:
            res = json.loads(self.request.body.decode())
        except json.JSONDecodeError:
            return dict(result=0, status=1, msg='Json Decode Error.')

        for key in key_list:
            if key not in res:
                raise MissingArgumentError(key)

        return Arguments(res)
