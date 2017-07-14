# coding:utf-8
"""Module of Backup"""

import re
import time
from hashlib import md5
from urllib.parse import urlencode

from utils import config


def creat_active_url(interface, email, add_time):
    """Create a super zhang active url."""
    random_code = config.login_secret.check_key
    time_str = time.ctime(add_time)
    md5str = md5((email + time_str + random_code).encode()).hexdigest()
    pub = dict(
        e=email,
        time=add_time,
        v=md5str, )
    result = interface + '?' + urlencode(pub)
    return result


def check_active_url(email, add_time, md5str):
    """Check a super zhang active url."""
    time_str = time.ctime(add_time)
    check_md5str = md5((email + time_str +
                        config.login_secret.check_key).encode()).hexdigest()
    return md5str == check_md5str


def check_email(email):
    """Check an email address format."""
    pattern = r'^[a-zA-Z0-9\._-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){1,3}$'
    return re.match(pattern, email)


def check_password(password):
    """Check a password string format."""
    pattern = r'^[a-zA-Z0-9_*]*$'
    return re.match(pattern, password)


def add_params_to_url(url, params):
    """Add parameters to a URL."""
    return url + '?' + urlencode(params)
