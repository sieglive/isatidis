# coding:utf-8
"""Module of Requests to Wondershare API"""
import json
import time
from datetime import datetime
from hashlib import md5
from io import BytesIO
from urllib.parse import parse_qs, unquote, urlencode, urlparse

import requests

from config import CFG as config


class WonderShareAPI:
    """Package of wondershare API."""

    def request(self, url, params=None, method='GET'):
        """Wondershare account request function."""
        info = urlparse(url)
        q_path = info.path + '?' + info.query if info.query else info.path
        print(params)
        params = params if params else {}
        q_url = info.scheme + '://' + info.netloc + self._encode_vc(
            q_path, params, method)

        if method == 'POST':
            response = requests.post(
                q_url, data=params, headers={'host': 'rest.wondershare.com'})
        else:
            response = requests.get(
                q_url, headers={'host': 'rest.wondershare.com'})

        if response.content != b'access denied!':
            try:
                res = json.loads(response.content.decode('utf-8'))
            except json.JSONDecodeError as exception:
                print(response.content)
                raise exception
        else:
            res = {'content': response.content.decode()}
        return res

    def _encode_vc(self, url, data, method='GET'):
        ws_key = config.login_secret.login_key.encode('latin1')
        ws_fp = config.login_secret.login_fp.encode('latin1')

        url_info = urlparse(url)
        if url_info.query:
            params = parse_qs(url_info.query)
            for i in params:
                params[i] = params[i][0]
        else:
            params = dict()

        params.update(data)
        ws_vc = self._create_vc(ws_key, ws_fp, params)

        if method == 'POST':
            params = {}

        params['key'] = ws_key
        params['vc'] = ws_vc

        url = url_info.path + '?' + urlencode(params)
        if url_info.query:
            url += '&' + url_info.query
        return url

    def _create_vc(self, ws_key, ws_fp, params):
        if isinstance(params, dict):
            keys = params.keys()
            for i in sorted(keys):
                params[i] = unquote(params[i])
            res = self._ksort_serialize(params)
        elif isinstance(params, str):
            res = params.encode('utf-8')
        else:
            res = b''
        return md5(ws_key + res + ws_fp).hexdigest()

    def _ksort_serialize(self, params):
        mystr = b'a:'
        key_list = params.keys()
        mystr += str(len(key_list)).encode('latin1') + b':{'
        for i in sorted(key_list):
            mystr += self._serialize(i)
            mystr += self._serialize(params[i])

        mystr += b'}'
        return mystr

    def _serialize(self, obj):
        if isinstance(obj, (int, float, bool)):
            return ('i:%i;' % obj).encode('latin1')
        if isinstance(obj, (str, bytes)):
            encoded_obj = obj
            if isinstance(obj, str):
                encoded_obj = obj.encode()
            bio = BytesIO()
            bio.write(b's:')
            bio.write(str(len(encoded_obj)).encode())
            bio.write(b':"')
            bio.write(encoded_obj)
            bio.write(b'";')
            return bio.getvalue()
        if obj is None:
            return b's:0:"";'
        raise TypeError('can\'t serialize %r as key' % type(obj))

    def create_datestamp(self, timestamp):
        """Create a date stamp for wondershare API."""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def modify_password(self, uid, password):
        """Request modify password."""
        info = self.request(
            'http://%s%s?%s' % (config.domain.login,
                                config.ws_api.modify_password, 'uid=%s' % uid),
            params=dict(email_pass=md5(password.encode()).hexdigest()),
            method='POST')

        if 'EditResult' in info and info['EditResult'] == 'yes':
            res = dict(result=1, status=0, msg='Modify Password Successfully.')
        else:
            error = info['error']
            res = dict(result=0, status=error['code'], msg=error['msg'])

        return res

    def register(self, email, password, first_name, last_name):
        """Request register interface of wondershare."""
        info = self.request(
            'http://%s%s' % (config.domain.login, config.ws_api.register),
            params=dict(
                firstName=first_name,
                lastName=last_name,
                email=email,
                email_pass=password,
                created=self.create_datestamp(time.time()), ),
            method='POST')

        if 'AddResult' in info and info['AddResult'] == 'yes':
            res = dict(result=1, status=0, msg='Register Successfully.')
        elif 'error' in info:
            error = info['error']
            res = dict(result=0, status=error['code'], msg=error['msg'])
        else:
            res = dict()

        return res

    def login(self, email, password):
        """Request log in interface of wondershare."""
        info = self.request(
            'http://%s%s' % (config.domain.login, config.ws_api.login),
            params={
                'username': email,
                'password': password,
            })

        if 'LoginResult' not in info:
            if 'error' in info and info['error'].get('code') == 470:
                res = dict(result=0, status=1, msg=info['error']['msg'])
            elif 'error' in info:
                res = dict(
                    result=0,
                    status=info['error'].get('code'),
                    msg='Unknown Error')
            else:
                res = dict(
                    result=0,
                    status=4999,
                    msg=info.get('content'))
        else:
            res = dict(result=1, status=0, msg=info['LoginResult']['message'])

        return res

    def fetch_user_info(self, email):
        """Request user information interface of wondershare."""
        info = self.request(
            'http://%s%s' % (config.domain.login, config.ws_api.user_info),
            params={
                'email': email,
            })
        if 'Member' in info:
            info = info['Member']['Info']
            res = dict(result=1, status=0, msg='Fetch success.')
            created_time = time.mktime(
                time.strptime(info['created'], '%Y-%m-%d %H:%M:%S'))
            res['data'] = dict(
                email=info['email'],
                register_time=created_time,
                appear_time=created_time,
                ws_id=int(info['uid']),
                company=info['company'],
                first_name=info['firstname'],
                last_name=info['lastname'], )
            return res
        else:
            res = dict(result=0, status=1, msg='Fetch failed.', data=info)
            return res

API = WonderShareAPI()
