# coding:utf-8
"""Module of Celery tools"""
import json
import os
import random
import time
import traceback
from functools import wraps


def dec2hex(dec_num, length=2):
    """turn a decimal number to hexadecimal number."""
    num = hex(dec_num)[2:]
    return '0' * (length - len(num)) + num


def spam_encode(params):
    """Encode params to a Spam format."""
    if not isinstance(params, dict):
        print(params)
        raise TypeError(f'Parameter should be a dict, not {type(params)}')
    if 'status' not in params:
        raise ValueError('Parameter should has key(\'status\').')
    if not isinstance(params['status'], int):
        raise ValueError('Status in parameter should be a integer.')
    if not 0 <= params['status'] <= 255:
        raise ValueError('Status in parameter should in [0, 255].')
    status = params.get('status')
    res = json.dumps(params)
    return dec2hex(status) + res


def spam_decode(spam_str):
    """Decode a Spam string."""
    print(spam_str)
    if not isinstance(spam_str, str):
        raise TypeError('Parameter is not str.')
    if len(spam_str) < 2:
        raise ValueError(
            'Parameter is not spam format str(short than 2 bytes).')
    status = int(spam_str[:2], 16)
    res = json.loads(spam_str[2:])
    if 'status' not in res:
        res['status'] = status
    else:
        res['status_out'] = status
    return res


def serial(func):
    """Serial the parameter after function and unserial the
    parameter before the function."""

    @wraps(func)
    def wrapper(params_dict, key_in, **kwargs):
        """Function that wrapped."""
        req = spam_decode(params_dict)
        if req.get('status') == 0:
            for arg in kwargs:
                if arg in req:
                    raise ValueError(f'Key "{arg}" is already in params.')
                else:
                    req[arg] = kwargs[arg]
            res = func(req, key_in)
            return spam_encode(res)
        elif 'status' not in req:
            raise ValueError('Key \'status\' not in request dict.')
        else:
            return params_dict

    return wrapper


def bindserial(func):
    """Serial the parameter after function and unserial the
    parameter before the function."""

    @wraps(func)
    def wrapper(self, params_dict, key_in, **kwargs):
        """Function that wrapped."""
        req = spam_decode(params_dict)
        if req.get('status') == 0:
            for arg in kwargs:
                if arg in req:
                    raise ValueError(f'Key {arg} is already in params.')
                else:
                    req[arg] = kwargs[arg]
            res = func(self, req, key_in)
            return spam_encode(res)
        elif 'status' not in req:
            raise ValueError('Key \'status\' not in request dict.')
        else:
            return params_dict

    return wrapper


def print_exception(exception=Exception('Exception')):
    """Used to print exception."""
    print('||||||||||||\n', '=\n', exception, '=' * 80)
    traceback.print_exc()
    print('=' * 80, '\n=', '\n||||||||||||')
    return 'fail', None


def figure_id(namespace='0000'):
    """Creat file id"""
    now = time.time()
    timep = hex(int(now * 1000))[2:]
    rands = random.randint(0, 65535)
    rands = f'{rands:04x}'
    return f'{namespace}-{timep[4:8]}-{timep[:4]}-{rands}-{timep[8:]}'


def extract_params(params_dict, key_list):
    """Get parameters from dictonary use the key in key list."""
    return [params_dict.get(key) for key in key_list]


def add_label(path, label):
    """Add a label into the place between the origin name and the ext."""
    return (f'{label}').join(os.path.splitext(path))


def change_ext(path, new_ext):
    """Change the extension name with a new one."""
    return os.path.splitext(path)[0] + new_ext


def basename(path):
    """Get the basename of the path."""
    return os.path.basename(path)
