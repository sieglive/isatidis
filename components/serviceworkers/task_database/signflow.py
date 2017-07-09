# coding:utf-8
"""Module of Table File Query Function."""

from sqlalchemy import desc

from models import SignFlow
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def insert_flow(flow_id,
                user_id,
                origin_file,
                initiate_time,
                logo=None,
                valid=1,
                subject=None,
                message=None,
                **kwargs):
    """Insert a signflow."""
    sess = kwargs.get('sess')
    new_flow = SignFlow(
        flow_id=flow_id,
        user_id=user_id,
        origin_file=origin_file,
        initiate_time=initiate_time,
        logo=logo,
        valid=valid,
        subject=subject,
        message=message)
    sess.add(new_flow)
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def query_flow_by_flow_id(flow_id, **kwargs):
    """Query a signflow by a flow ID."""
    sess = kwargs.get('sess')

    flow = sess.query(SignFlow).filter(SignFlow.flow_id == flow_id).first()

    if flow:
        result = flow.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def query_flow_by_origin_file(origin_file, **kwargs):
    """Query a signflow by a origin file."""
    sess = kwargs.get('sess')
    limit = kwargs.get('limit')

    flow_list = sess.query(SignFlow).filter(
        SignFlow.origin_file == origin_file)

    if limit:
        flow_list = flow_list.limit(limit)
    else:
        flow_list = flow_list.all()

    if flow_list:
        result = [flow.to_dict() for flow in flow_list]
    else:
        result = None
    return result


@app.task
@exc_handler
def query_flow_by_user_id(user_id, **kwargs):
    """Query flow with user ID."""
    sess = kwargs.get('sess')
    limit = kwargs.get('limit')

    flow_list = sess.query(SignFlow).filter(
        SignFlow.user_id == user_id).order_by(desc(SignFlow.initiate_time))

    if limit:
        flow_list = flow_list.limit(limit)
    else:
        flow_list = flow_list.all()

    if flow_list:
        result = [flow.to_dict() for flow in flow_list]
    else:
        result = None
    return result


@app.task
@exc_handler
def update_flow_info(flow_id, **kwargs):
    """Update info of an account."""
    sess = kwargs.get('sess')
    invert_dict = dict(
        notice_level=SignFlow.notice_level,
        access_code=SignFlow.access_code,
        logo=SignFlow.logo,
        subject=SignFlow.subject,
        message=SignFlow.message)

    key_list = list(invert_dict.keys())
    for key in key_list:
        if key not in kwargs:
            del invert_dict[key]

    update_dict = dict([(invert_dict[k], kwargs[k]) for k in invert_dict])
    if update_dict:
        update_num = sess.query(SignFlow).filter(
            SignFlow.flow_id == flow_id).update(update_dict)
        result = update_num
        sess.commit()
    else:
        result = None

    return result


TASK_DICT = dict(
    insert_flow=insert_flow,
    query_flow_by_flow_id=query_flow_by_flow_id,
    query_flow_by_origin_file=query_flow_by_origin_file,
    query_flow_by_user_id=query_flow_by_user_id,
    update_flow_info=update_flow_info)
