# coding:utf-8
"""Module of Table File Query Function."""

import json
import time
from uuid import uuid1 as uuid

from sqlalchemy import desc

from models import Signature
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_signature_by_user_id(user_id, limit, **kwargs):
    """Query sign image by user id."""
    sess = kwargs.get('sess')
    sign_list = sess.query(Signature).filter(
        Signature.user_id == user_id).filter(
            Signature.valid == 1).order_by(
                desc(Signature.time)).limit(limit)

    if sign_list:
        result = [sign.to_dict() for sign in sign_list]
    else:
        result = None

    for sign in result:
        if 'image_type' in sign:
            sign['image_type'] = sign['image_type'].name
    return result


@app.task
@exc_handler
def query_signature_by_signature_id(signature_id, **kwargs):
    """Query sign image by user id."""
    sess = kwargs.get('sess')
    sign_image = sess.query(Signature).filter(
        Signature.signature_id == signature_id).filter(
            Signature.valid == 1).first()

    result = sign_image.to_dict()
    if 'image_type' in result:
        result['image_type'] = result['image_type'].name

    return result


@app.task
@exc_handler
def insert_signature(signature_id, user_id, path, image_type, **kwargs):
    """Query sign image by user id."""
    sess = kwargs.get('sess')
    sess.add(
        Signature(
            signature_id=signature_id,
            user_id=user_id,
            path=path,
            image_type=image_type,
            time=int(time.time())))
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_sign_valid_by_list(signature_list, **kwargs):
    """Update sign image by user id."""
    sess = kwargs.get('sess')
    for sign in signature_list:
        sess.query(Signature).filter(Signature.signature_id == sign).update({
            Signature.valid:
            0
        })
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_sign_valid_by_sign_id(signature_id, **kwargs):
    """Update sign image by user id."""
    sess = kwargs.get('sess')
    sess.query(Signature).filter(
        Signature.signature_id == signature_id).update({
            Signature.valid: 0
        })
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


TASK_DICT = dict(
    query_signature_by_signature_id=query_signature_by_signature_id,
    query_signature_by_user_id=query_signature_by_user_id,
    insert_signature=insert_signature,
    update_sign_valid_by_list=update_sign_valid_by_list,
    update_sign_valid_by_sign_id=update_sign_valid_by_sign_id, )
