# coding:utf-8
"""Module of Table File Query Function."""

import time

from sqlalchemy import and_
from sqlalchemy import desc

from models import Flower, User
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_flower_by_flow_id(flow_id, **kwargs):
    """Query flower by flow id."""
    sess = kwargs.get('sess')
    order = kwargs.get('order')
    join_user = kwargs.get('join_user')

    if join_user:
        flower_list = sess.query(
            Flower, User
        ).join(
            User,
            User.user_id == Flower.user_id
        ).filter(
            Flower.flow_id == flow_id)
    else:
        flower_list = sess.query(Flower).filter(Flower.flow_id == flow_id)

    if order:
        if isinstance(order, int):
            flower_list = flower_list.filter(Flower.order == order)
        else:
            flower_list = flower_list.filter(Flower.order in order)

    flower_list = flower_list.order_by(
        desc(Flower.order)
    ).all()

    if flower_list:
        if join_user:
            result = [dict(flower[0].to_dict(), **flower[1].to_dict())
                      for flower in flower_list]
        else:
            result = [flower.to_dict() for flower in flower_list]
    else:
        result = None
    return result


@app.task
@exc_handler
def query_flower_by_flower_id(flower_id, **kwargs):
    """Query flower by flower id."""
    sess = kwargs.get('sess')

    flower = sess.query(Flower).filter(Flower.flower_id == flower_id).first()

    if flower:
        result = flower.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def query_flower_by_flow_and_user(flow_id, user_id, **kwargs):
    """Query flower by flower id."""
    sess = kwargs.get('sess')

    flower = sess.query(Flower).filter(
        and_(Flower.flow_id == flow_id, Flower.user_id == user_id)).first()

    if flower:
        result = flower.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def insert_flower(flower_id,
                  flow_id,
                  email,
                  user_id=None,
                  role=1,
                  order=0,
                  **kwargs):
    """Insert a flower."""
    subject = kwargs.get('subject')
    message = kwargs.get('message')
    sess = kwargs.get('sess')
    new_flower = Flower(
        flower_id=flower_id,
        flow_id=flow_id,
        user_id=user_id,
        email=email,
        role=role,
        order=order,
        subject=subject,
        message=message,
        update_time=int(time.time()))
    sess.add(new_flower)
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def insert_flower_by_list(flow_id, email_list, **kwargs):
    """Insert flower with list."""
    sess = kwargs.get('sess')
    now = int(time.time())
    insert_sql = ', '.join(
        f'(UUID(), "{flow_id}", "{email}", 0, 0, 0, {now})'
        for email in email_list)

    sql = (f'INSERT IGNORE INTO  '
           f'flower( '
           f'    `flower_id`, '
           f'    `flow_id`, '
           f'    `email`, '
           f'    `role`, '
           f'    `signed`, '
           f'    `refuse_notice`, '
           f'    `update_time`) '
           f'VALUES {insert_sql};')
    print(sql)
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_userid_by_flowid(flow_id, **kwargs):
    """Update flower userID by flowID."""
    sess = kwargs.get('sess')
    sql = (f'UPDATE flower, `user` '
           f'SET flower.user_id = `user`.user_id, '
           f'flower.update_time = UNIX_TIMESTAMP() '
           f'WHERE flower.email = `user`.email '
           f'AND flower.flow_id = "{ flow_id }";')
    print(sql)
    result = sess.execute(sql)
    print(result)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_role_by_list(flow_id,
                               email_list,
                               mod,
                               action='add',
                               **kwargs):
    """Update flower role by list."""
    opmod = f'~({mod}) & 0b11111111'
    if action == 'add':
        opt1 = '|'
        opt2 = '&'
    elif action == 'delete':
        opt1 = '&'
        opt2 = '|'
        opmod, mod = mod, opmod

    sess = kwargs.get('sess')
    email_list = ', '.join(
        [f'"{email}"' for email in email_list])

    sql = (f'UPDATE flower '
           f'SET flower.role = IF( '
           f'    flower.email IN ({email_list}), '
           f'    flower.role {opt1} ({mod}), '
           f'    flower.role {opt2} ({opmod})), '
           f'    flower.update_time = UNIX_TIMESTAMP() '
           f'WHERE flower.flow_id = "{flow_id}";')

    print(sql)
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_role_by_flow_id(flow_id, mod, action='add', **kwargs):
    """Update flower role by flow id."""
    if action == 'add':
        opt = '|'
    elif action == 'delete':
        opt = '&'
        mod = f'~({ mod }) & 0b11111111'
    sess = kwargs.get('sess')
    sql = (f'UPDATE flower '
           f'SET flower.role = flower.role { opt } ({ mod }), '
           f'    flower.update_time = UNIX_TIMESTAMP() '
           f'WHERE flower.`flow_id` = ({ flow_id });')
    print(sql)
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_order_by_list(flow_id, flower_list, **kwargs):
    """Update flower order by list."""
    sess = kwargs.get('sess')
    sql = (f'UPDATE flower '
           f'SET flower.`order` = 0, '
           f'    flower.update_time = UNIX_TIMESTAMP() '
           f'WHERE flower.`flow_id` = "{ flow_id }"; ')
    sql += ' '.join([(f'UPDATE flower '
                      f'SET flower.`order` = { order }, '
                      f'    flower.update_time = UNIX_TIMESTAMP() '
                      f'WHERE flower.`flow_id` = "{ flow_id }" '
                      f'AND flower.`email` = "{ email }";')
                     for email, order in flower_list])
    print(sql)
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_signed_status(flow_id, user_id, status, **kwargs):
    """Update flower sign status by flower ID."""
    sess = kwargs.get('sess')
    sess.query(
        Flower
    ).filter(
        Flower.flow_id == flow_id
    ).filter(
        Flower.user_id == user_id
    ).update({
        Flower.signed:
        status,
        Flower.update_time:
        int(time.time())
    })
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_flower_refuse_notice(flow_id, user_id, refuse_notice, **kwargs):
    """Update flower sign status by flower ID."""
    sess = kwargs.get('sess')
    sess.query(
        Flower
    ).filter(
        Flower.flow_id == flow_id
    ).filter(
        Flower.user_id == user_id
    ).update({
        Flower.refuse_notice:
        refuse_notice,
        Flower.update_time:
        int(time.time())
    })
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


TASK_DICT = dict(
    query_flower_by_flow_id=query_flower_by_flow_id,
    query_flower_by_flower_id=query_flower_by_flower_id,
    query_flower_by_flow_and_user=query_flower_by_flow_and_user,
    insert_flower=insert_flower,
    insert_flower_by_list=insert_flower_by_list,
    update_flower_userid_by_flowid=update_flower_userid_by_flowid,
    update_flower_order_by_list=update_flower_order_by_list,
    update_flower_role_by_flow_id=update_flower_role_by_flow_id,
    update_flower_role_by_list=update_flower_role_by_list,
    update_flower_refuse_notice=update_flower_refuse_notice,
    update_flower_signed_status=update_flower_signed_status, )
