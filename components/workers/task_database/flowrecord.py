# coding:utf-8
"""Module of Table File Query Function."""
import time

from sqlalchemy import and_, desc

from models import SignFlowRecord
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def insert_flow_record(flow_id, action, operate_user, operate_email,
                       operate_ip, operate_time, **kwargs):
    """Insert a record to database."""
    sess = kwargs.get('sess')

    sql = (f'INSERT IGNORE INTO '
           f'signflow_record( '
           f'    `flow_id`, '
           f'    `action`, '
           f'    `operate_user`, '
           f'    `operate_email`, '
           f'    `operate_ip`, '
           f'    `operate_time`) '
           f'VALUES ("{flow_id}", "{action}", "{operate_user}", '
           f'"{operate_email}", "{operate_ip}", {operate_time});')
    print(sql)
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully.')


@app.task
@exc_handler
def update_flow_record_operate_time(flow_id, **kwargs):
    """Update time of a completed record."""
    sess = kwargs.get('sess')
    sess.query(SignFlowRecord).filter(
        SignFlowRecord.flow_id == flow_id).filter(
            SignFlowRecord.action == 'completed').update({
                SignFlowRecord.operate_time:
                int(time.time() + 1)
            })
    sess.commit()
    return dict(result=1, status=0, msg='Successfully.')


@app.task
@exc_handler
def query_flow_record(flow_id, **kwargs):
    """Query record of a flow."""
    sess = kwargs.get('sess')
    record_list = sess.query(SignFlowRecord).filter(
        SignFlowRecord.flow_id == flow_id).order_by(
            SignFlowRecord.operate_time).all()

    result = [record.to_dict() for record in record_list]

    for record in result:
        record['action'] = record['action'].name
    return result


@app.task
@exc_handler
def query_flow_last_record(flow_id, **kwargs):
    """Query record of a flow."""
    sess = kwargs.get('sess')
    action = kwargs.get('action')

    record = sess.query(SignFlowRecord).filter(
        SignFlowRecord.flow_id == flow_id)

    if action:
        record = record.filter(
            SignFlowRecord.action == action)

    record = record.order_by(
            desc(SignFlowRecord.operate_time)).first()

    if record:
        result = record.to_dict()
        result['action'] = result['action'].name
    else:
        result = None
    return result


@app.task
@exc_handler
def query_agreement_record(flow_id, user_id, **kwargs):
    """Query agreement of a flow."""
    sess = kwargs.get('sess')
    record = sess.query(SignFlowRecord).filter(
        SignFlowRecord.flow_id == flow_id).filter(
            SignFlowRecord.operate_user == user_id).filter(
                SignFlowRecord.action == 'agreement').first()

    if record:
        result = record.to_dict()
        result['action'] = result['action'].name
    else:
        result = None

    return result


TASK_DICT = dict(
    update_flow_record_operate_time=update_flow_record_operate_time,
    insert_flow_record=insert_flow_record,
    query_flow_record=query_flow_record,
    query_flow_last_record=query_flow_last_record,
    query_agreement_record=query_agreement_record, )
