#! /env/python3
# coding:utf-8
"""Main Loop Module of Isatis DB server."""
from tornado import web, gen, httpserver, ioloop
from tornado.options import options

from views.base import BaseHandler


class IndexHandler(BaseHandler):
    """Index Page."""
    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        self.render('text.html')


def isatis():
    """Main Loop of Isatis db server."""
    options.parse_command_line()
    handlers = [
        (r'/', IndexHandler),
        (r'/back/?', IndexHandler),
    ]
    tornado_app = web.Application(
        handlers=handlers,
        template_path='templates',
    )
    tornado_server = httpserver.HTTPServer(
        tornado_app,
    )
    tornado_server.listen(7717)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    isatis()
