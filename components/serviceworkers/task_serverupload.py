# coding:utf-8
"""PDF interface module.
    This is a dustbin of magic code. If you need, rewrite it by yourself."""
import base64
import binascii

from . import Oss, Tasks, config
from .manager import APP as app

OSS = Oss(endpoint=config.oss.end_point, bucket=config.oss.bucket)


@app.task
def check_image_exists(file_id, page):
    """Check Image if exists."""
    path = f'files/{file_id}/{page}.jpg'
    return OSS.object_exists(path)


@app.task
def upload_from_stream(image, remotepath):
    """upload a file by stream"""

    try:
        image_bytes = base64.b64decode(image)
    except binascii.Error:
        return dict(
            result=0, status=1, msg='Argument "image" is not base64 code.')
    print(remotepath)
    a = OSS.put_from_stream(image_bytes, remotepath)
    print(a)

    return dict(result=1, status=0, msg='Successfully', data=None)


TASKS = Tasks(
    dict(
        upload_from_stream=upload_from_stream,
        check_image_exists=check_image_exists))
