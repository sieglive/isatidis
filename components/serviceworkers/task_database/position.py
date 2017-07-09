# coding:utf-8
"""Module of Table File Query Function."""

import json
import time
import traceback
from uuid import uuid1 as uuid

from models import Position
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_position_by_flow_id(flow_id, **kwargs):
    """Query position by flow id."""
    sess = kwargs.get('sess')

    pos_type = kwargs.get('pos_type')
    pos_signer = kwargs.get('pos_signer')
    pos_setor = kwargs.get('pos_setor')
    pos_result = sess.query(Position).filter(Position.pos_flow == flow_id)

    if pos_type:
        pos_result = pos_result.filter(Position.pos_type == pos_type)
    if pos_signer:
        pos_result = pos_result.filter(Position.pos_signer == pos_signer)
    if pos_setor:
        pos_result = pos_result.filter(Position.pos_setor == pos_setor)

    pos_list = pos_result.all()

    if pos_list:
        result = [pos.to_dict() for pos in pos_list]
        for pos in result:
            if pos['sign_type']:
                pos['sign_type'] = pos['sign_type'].name
            if pos['pos_type']:
                pos['pos_type'] = pos['pos_type'].name
    else:
        result = None
    return result


@app.task
@exc_handler
def insert_position_by_list(flow_id, pos_list, pos_ip, **kwargs):
    """Insert position by a list."""
    sess = kwargs.get('sess')
    sess.query(Position).filter(Position.pos_flow == flow_id).delete()

    for pos in pos_list:
        if 'pos_setor' not in pos:
            return dict(
                result=0, status=1, msg='You need set setor for a position.')
        if 'pos_signer' not in pos:
            return dict(
                result=0, status=1, msg='You need set signer for a position.')

        try:
            pos_params = json.dumps(pos.get('pos_params'))
        except json.JSONDecodeError:
            return dict(
                result=0, status=1, msg='Can\'t encode parameters to json.')
        except:
            traceback.print_exc()
            return dict(
                result=0, status=255, msg='Unknown Error.')

        sess.add(
            Position(
                pos_id=uuid(),
                pos_flow=flow_id,
                pos_params=pos_params,
                pos_type=pos.get('pos_type'),
                pos_setor=pos.get('pos_setor'),
                pos_signer=pos.get('pos_signer'),
                set_time=pos['set_time'] if pos.get('set_time') else int(
                    time.time()),
                sign_type=pos.get('sign_type'),
                sign_content=pos.get('sign_content'),
                sign_time=pos.get('sign_time'),
                sign_ip=pos_ip if pos.get('sign_content') else ''))
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_position_by_list(sign_list, sign_ip, **kwargs):
    """Insert position by flow ID."""
    sess = kwargs.get('sess')

    for sign in sign_list:
        pos_id = sign.get('pos_id')
        update_sess = sess.query(Position).filter(Position.pos_id == pos_id)
        update_dict = {Position.sign_ip: sign_ip}
        if sign.get('sign_type'):
            update_dict[Position.sign_type] = sign.get('sign_type')
        if sign.get('sign_content'):
            update_dict[Position.sign_content] = sign.get('sign_content')
        if sign.get('sign_time'):
            update_dict[Position.sign_time] = sign.get('sign_time')
        else:
            update_dict[Position.sign_time] = int(time.time())
        update_sess.update(update_dict)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


TASK_DICT = dict(
    query_position_by_flow_id=query_position_by_flow_id,
    insert_position_by_list=insert_position_by_list,
    update_position_by_list=update_position_by_list)
