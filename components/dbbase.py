# coding:utf-8
"""Base module for other views' modules."""
import json
import sys

from tornado import gen
from tornado.web import HTTPError, MissingArgumentError, RequestHandler

from utils import utils
from utils.utils import Arguments
from views import config

STATUS_DICT = dict([
    (4001, 'Username or password is invalid'),
    (4002, 'Account is inactivated.'),
    (4003, 'Account not exists.'),
])


class ParseJSONError(HTTPError):
    """Exception raised by `BaseHandler.parse_json`.

    This is a subclass of `HTTPError`, so if it is uncaught a 400 response
    code will be used instead of 500 (and a stack trace will not be logged).
    """

    def __init__(self, doc):
        super(ParseJSONError, self).__init__(
            400, 'ParseJSONError. Decode JSON data in request body failed.')
        self.doc = doc


class BaseHandler(RequestHandler):
    """Custom handler for other views module."""
    # Set the public head here.
    # pub_head = dict(
    #     version='?v=20160301&t=' + str(time.time()),
    #     base_url=options.BASE_URL,
    #     base_static_url=options.BASE_STATIC_URL,
    #     base_resource_url=options.BASE_RESOURCE_URL,
    # )

    # Rewrite abstract method
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def put(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def delete(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def head(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def options(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def patch(self, *args, **kwargs):
        self.write('405: Method Not Allowed')

    @gen.coroutine
    def data_received(self, chunk):
        self.write('405: Method Not Allowed')

    # # Get the argument if it is exist.
    # def try_to_get_arg(self, name, default=None):
    #     try:
    #         return self.get_argument(name)
    #     except MissingArgumentError:
    #         return default

    # # Get the current user from cookie.
    # def get_current_user(self):
    #     q_user = self.get_secure_cookie('user')
    #     if isinstance(q_user, bytes):
    #         q_user = q_user.decode()
    #     return q_user

    # # Set current user to cookie.
    # def set_current_user(self, username):
    #     self.set_secure_cookie(
    #         'user',
    #         username,
    #         expires=time.time() + options.EXPIRE_TIME,
    #         domain=options.DOMAIN
    #     )

    # # Get user information from cookie.
    # def get_parameters(self):
    #     q_params = self.get_secure_cookie('params')
    #     if q_params:
    #         q_params = json.loads(q_params.decode())
    #     else:
    #         q_params = dict(
    #             user_number=0,
    #             user_type=0,
    #             uid=0,
    #         )
    #     return q_params

    # # Set user information to the cookie.
    # def set_parameters(self, params, expire_time=1800):
    #     self.set_secure_cookie(
    #         'params',
    #         json.dumps(params),
    #         expires=time.time() + expire_time,
    #         domain=options.DOMAIN
    #     )

    # # Get the user name and password from cookie.
    # def get_password(self):
    #     q_params = self.get_secure_cookie('spam')
    #     if q_params:
    #         q_params = json.loads(q_params.decode())
    #     else:
    #         q_params = dict(
    #             username='',
    #             password='',
    #         )
    #     return q_params

    # # Set the user name and password to cookie.
    # def set_password(self, params, expire_time=2592000):
    #     self.set_secure_cookie(
    #         'spam',
    #         json.dumps(params),
    #         expires=time.time() + expire_time,
    #         domain=options.DOMAIN
    #     )

    # Return public code 0 and status 0 with an error message.
    def dump_fail_data(self,
                       msg,
                       exc_doc=None,
                       status=1,
                       mongo_client=None,
                       record_id=None,
                       update_dict=None,
                       *_args,
                       **_kwargs):
        """assemble and return error data."""
        if mongo_client and record_id:
            if not update_dict:
                update_dict = dict()
            update_dict['msg'] = msg
            update_dict['exc_doc'] = exc_doc
            mongo_client.update_one(
                dict(_id=record_id), {'$set': update_dict})
        res = dict(result=0, status=status,
                   exc_doc=exc_doc, msg=msg, ex_data=_kwargs.get('ex_data'))
        self.finish_with_json(res)
        return

    # def check_json_args(self, data, key_list):
    #     """Check if data match given key list."""
    #     for key in key_list:
    #         if key not in data:
    #             return False
    #         else:
    #             return True

    def parse_json_arguments(self, key_list):
        """Parse JSON argument like `get_argument`."""
        try:
            if config.debug:
                sys.stdout.write('\n\n' + '>' * 80)
                sys.stdout.write('\n' + (f'Input: '
                                         f'{self.request.method} '
                                         f'{self.request.path}') + '\n\n')
                sys.stdout.write(self.request.body.decode()[:500])
                sys.stdout.write('\n\n' + '>' * 80 + '\n')
                sys.stdout.flush()
            req = json.loads(self.request.body.decode('utf-8'))
        except json.JSONDecodeError as exception:
            # self.dump_fail_data(
            #     exc_doc=exception.doc, msg=exception.args[0], status=1)
            sys.stdout.write(self.request.body.decode())
            sys.stdout.write('\n')
            sys.stdout.flush()
            raise ParseJSONError(exception.doc)

        if not isinstance(req, dict):
            sys.stdout.write(self.request.body.decode())
            sys.stdout.write('\n')
            sys.stdout.flush()
            raise ParseJSONError('Req should be a dictonary.')

        for key in list(req.keys()):
            req[utils.camel_to_underline(key)] = req[key]

        for key in key_list:
            if key not in req:
                sys.stdout.write(self.request.body.decode())
                sys.stdout.write('\n')
                sys.stdout.flush()
                raise MissingArgumentError(key)

        req['user_ip'] = self.request.remote_ip

        return Arguments(req)

    def finish_with_json(self, data):
        """Turn data to JSON format before finish."""
        if config.debug:
            sys.stdout.write('' + '-' * 80)
            sys.stdout.write('\n' + (f'Output: '
                                     f'{self.request.method} '
                                     f'{self.request.path}') + '\n\n')
            sys.stdout.write(str(data))
            sys.stdout.write('\n\n' + '-' * 80 + '\n\n')
            sys.stdout.flush()
        self.finish(json.dumps(data).encode())

    def write_with_json(self, data):
        """Turn data to JSON format before write."""
        self.write(json.dumps(data).encode())

    # # Bind function to the config.
    # @gen.coroutine
    # def waiting_upload(self, func, args=None, kwargs=None):
    #     result = yield self.waiting_result(
    #         func, args=args, kwargs=kwargs, queue=options.queue_upload)
    #     return result

    # @gen.coroutine
    # def waiting_payment(self, func, args=None, kwargs=None):
    #     result = yield self.waiting_result(
    #         func, args=args, kwargs=kwargs, queue=options.queue_payment)
    #     return result

    # @gen.coroutine
    # def waiting_query(self, func, args=None, kwargs=None):
    #     result = yield self.waiting_result(
    #         func, args=args, kwargs=kwargs, queue=options.queue_query)
    #     return result

    # Waiting result of celery task without blocking.
    @gen.coroutine
    def waiting_result(self, func, args=None, kwargs=None):
        """Method to waiting celery result."""
        async_task = func.apply_async(args=args, kwargs=kwargs)

        while True:
            if async_task.status in ['PENDING', 'PROGRESS']:
                yield gen.sleep(config.waiting_sleep_time)
            elif async_task.status in ['SUCCESS', 'FAILURE']:
                break
            else:
                print('\n\nUnknown status:\n', async_task.status, '\n\n\n')
                break

        if async_task.status != 'SUCCESS':
            print(async_task.status, async_task.result)
            print(async_task)
            return dict(result=0, status=1, data=async_task.result)
        else:
            return async_task.result

    # # For the important task, retry if the task failed.
    # @gen.coroutine
    # def retry(self, query, queue, args=None, kwargs=None):
    #     action = 'fail'
    #     result = None
    #     for i in range(5):
    #         action, result = yield self.waiting_result(
    #             query(
    #                 args=args,
    #                 kwargs=kwargs,
    #                 retry=False,
    #                 queue=queue
    #             ))
    #         if action != 'fail':
    #             break
    #         yield gen.sleep(0.4)

    #     return action, result
