# coding:utf-8
"""Base Module of other View Modules."""
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """Rewrite some method of RequestHandler."""

    def get(self, *_args, **_kwargs):
        pass

    def put(self, *_args, **_kwargs):
        pass

    def post(self, *_args, **_kwargs):
        pass

    def delete(self, *_args, **_kwargs):
        pass

    def head(self, *_args, **_kwargs):
        pass

    def options(self, *_args, **_kwargs):
        pass

    def data_received(self, chunk):
        pass

