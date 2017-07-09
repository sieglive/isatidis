# coding:utf-8
"""Module of Cart Securit"""
import base64
import json
import sys

from Crypto.Cipher import AES

_KEY = b'B[COi%x#rOHVr6[+                '
_IV = b'5NlFI(CaTYOvGVXx'


def cart_decode(data):
    """Cart decode function."""
    data = data.replace('-', '+').replace('_', '/')
    mod4 = len(data) % 4
    data += '====' [:mod4]
    result = base64.b64decode(data)

    cryptor = AES.new(key=_KEY, mode=AES.MODE_CBC, IV=_IV)
    plain_text = cryptor.decrypt(result).rstrip(b'\0')

    json_object = json.loads(plain_text.decode())

    return json_object


def cart_encode(json_object):
    """Cart encode function."""
    plain_text = json.dumps(json_object).encode()

    rest_blank = 16 - len(plain_text) % 16
    plain_text += b'\0' * rest_blank

    cryptor = AES.new(key=_KEY, mode=AES.MODE_CBC, IV=_IV)
    result = cryptor.encrypt(plain_text)

    data = base64.b64encode(result).decode()
    data = data.replace('+', '-').replace('/', '_').replace('=', '')

    return data


def _test():
    data = 'GQ1hkBr1f7YMgwN26cVV6359uLS0_ob6bhR0RFBF5mxOdNHlzx9EDlkKbR5vMauM' \
        'cie64CcMzJlR054ELpLeoD8A1yJLJAtr886v9UXEHEq9lf3dXFU1MSK2BXBG7FSg' \
        'FUdR1dx24Hb7MNJHS52m5m5L_0Fd0bexUjRA-0snIxbdsBDQ02HuOnfgcPGruAil' \
        'XXp4zFmI9jdabMPjxLRYHpZxKYvFjpkaCUqiA5pgXS4ZNlDlq3VV9r1EJl7TCXT2' \
        'RuR9xS2uaT_QwAwrAfASqaaZ3JDFDwMytC5dIRoAvY6PTXFXo1JLFvNX9HWJUSWa' \
        'Cq-u1mpDfNVU1rRfRQwVn-7WMF9ux0Q_k8S1LOlJDlmwwN-uak5PhccLG3nZrZNu' \
        '9V6Cl78WN22meNpT4wq2Q8uuo1lnohTbaiBZf1dO0_A3ut8ISOPH_lVf3yMc8JBz' \
        'fFdagdQPiq4jJ2SUSXw-Xg'

    json_object = cart_decode(data)

    new_data = cart_encode(json_object)

    new_object = cart_decode(new_data)

    json.dump(json_object, sys.stdout, sort_keys=True)
    print()
    json.dump(new_object, sys.stdout, sort_keys=True)
    print()
    print(json_object == new_object)


if __name__ == '__main__':
    _test()
