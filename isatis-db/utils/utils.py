# coding:utf-8
"""Module of some useful tools."""
import random
import re
import time
from hashlib import md5


def underline_to_camel(underline_format):
    """Turn a underline format string to a camel format string."""
    pattern = re.split(r'_', underline_format)
    for i in range(1, len(pattern)):
        pattern[i] = pattern[i].capitalize()
    return ''.join(pattern)


def camel_to_underline(camel_format):
    """Turn a camel format string to a underline format string."""
    pattern = re.split(r'([A-Z])', camel_format)
    result = pattern[:1]
    result += [
        pattern[i].lower() + pattern[i + 1].lower()
        for i in range(1, len(pattern), 2)
    ]
    return '_'.join(result)


def create_random_code():
    """create a random code with time and md5"""
    return md5(str(time.time()).encode()).hexdigest()


def figure_id(namespace='0000'):
    """Creat file id"""
    now = time.time()
    timep = hex(int(now * 1000))[2:]
    rands = random.randint(0, 65536)
    rands = f'{rands:04x}'
    return f'{namespace}-{timep[4:8]}-{timep[:4]}-{rands}-{timep[8:]}'


class Tasks:
    """Manager class of tasks."""

    def __init__(self, params):
        if isinstance(params, dict):
            self.tasks = params
        else:
            raise TypeError(
                f"Arguments data should be a 'dict' not {type(params)}.")

    def __getattr__(self, task_name):
        task = self.tasks.get(task_name)
        if task is None:
            raise KeyError(task_name)
        else:
            return task

    def __iter__(self):
        for i in self.tasks:
            yield i

    def __getitem__(self, name):
        task = self.tasks.get(name)
        if task is None:
            raise KeyError(name)
        else:
            return task

    def as_dict(self):
        """Return the task dictionary."""
        return self.tasks

    def keys(self):
        """Return the keys of the task dictionary."""
        return self.tasks.keys


class Arguments(object):
    """Class to manage arguments of a requests."""

    def __init__(self, params):
        if isinstance(params, dict):
            self.arguments = params
        else:
            raise TypeError(
                f"Arguments data should be a 'dict' not {type(params)}.")

    def __getattr__(self, name):
        attr = self.arguments.get(name)
        return attr

    def __getitem__(self, name):
        attr = self.arguments.get(name)
        if attr is None:
            raise KeyError(name)
        else:
            return attr

    def as_dict(self):
        """Return all the arguments as a dictonary."""
        return self.arguments

    def add(self, key, value):
        """Add a variable to args."""
        self.arguments[key] = value
