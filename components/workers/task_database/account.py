# coding:utf-8
"""Module of Table Account Query Function."""

import time
from uuid import uuid1

from models import SignFlow, User
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_account(**kwargs):
    """Query account info."""
    sess = kwargs.get('sess')
    email = kwargs.get('email')
    user_id = kwargs.get('user_id')

    account = sess.query(User)

    if user_id:
        account = account.filter(User.user_id == user_id)
    elif email:
        account = account.filter(User.email == email)
    else:
        return None

    account = account.first()

    if account:
        result = account.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def query_account_by_user_id(user_id, **kwargs):
    """Query account info."""
    sess = kwargs.get('sess')

    account = sess.query(User).filter(User.user_id == user_id).first()

    if account:
        result = account.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def query_account_by_flow_id(flow_id, **kwargs):
    """Query account info."""
    sess = kwargs.get('sess')

    account = sess.query(SignFlow, User).join(
        User, User.user_id == SignFlow.user_id).filter(
            SignFlow.flow_id == flow_id).first()

    if account:
        result = dict(account[0].to_dict(), **account[1].to_dict())
    else:
        result = None
    return result


@app.task
@exc_handler
def insert_account(old_ws_id,
                   email,
                   active_code=None,
                   expire_time=0,
                   register_time=0,
                   appear_time=0,
                   active_status=0,
                   valid=1,
                   permission=0,
                   first_name=None,
                   last_name=None,
                   company=None,
                   title=None,
                   country=None,
                   avatar=None,
                   company_logo=None,
                   **kwargs):
    """Insert an account."""
    sess = kwargs.get('sess')
    new_user = User(
        user_id=uuid1(),
        old_ws_id=old_ws_id,
        email=email,
        active_code=active_code,
        expire_time=expire_time,
        register_time=register_time,
        appear_time=appear_time,
        active_status=active_status,
        valid=valid,
        permission=0,
        first_name=first_name,
        last_name=last_name,
        company=company,
        title=title,
        country=country,
        avatar=avatar,
        company_logo=company_logo)
    sess.add(new_user)
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def insert_account_by_list(email_list, **kwargs):
    """Insert a mount of account."""
    sess = kwargs.get('sess')
    now = kwargs.get('appear_time')
    now = int(time.time()) if not now else now
    insert_sql = ', '.join(
        f'(UUID(), "{email}", {now}, 0, 0, 0, 1)' for email in email_list)

    sql = (f'INSERT IGNORE INTO  '
           f'user( '
           f'    `user_id`, '
           f'    `email`, '
           f'    `appear_time`, '
           f'    `active_status`, '
           f'    `expire_time`, '
           f'    `permission`, '
           f'    `valid`) '
           f'VALUES {insert_sql};')
    sess.execute(sql)
    sess.commit()
    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_account_status(email, status, **kwargs):
    """Update status of an account."""
    sess = kwargs.get('sess')
    account = sess.query(User).filter(User.email == email).update({
        User.active_status:
        status
    })
    result = account
    sess.commit()
    return result


@app.task
@exc_handler
def update_account_expire_time(email, expire_time, **kwargs):
    """Update expire time of an account."""
    sess = kwargs.get('sess')
    account = sess.query(User).filter(User.email == email).update({
        User.expire_time:
        expire_time
    })
    result = account
    sess.commit()
    return result


@app.task
@exc_handler
def update_acount_info(**kwargs):
    """Update info of an account."""
    sess = kwargs.get('sess')
    user_id = kwargs.get('user_id')
    email = kwargs.get('email')
    if not user_id and not email:
        return dict(
            result=0,
            status=1,
            msg=('Missing Argument, '
                 'either "user_id" or "email" should in arguments.'),
            data=None
        )
    invert_dict = dict(
        old_ws_id=User.old_ws_id,
        active_code=User.active_code,
        register_time=User.register_time,
        first_name=User.first_name,
        last_name=User.last_name,
        company=User.company,
        title=User.title,
        country=User.country,
        avatar=User.avatar,
        company_logo=User.company_logo)

    key_list = list(invert_dict.keys())
    for key in key_list:
        if key not in kwargs:
            del invert_dict[key]

    update_dict = dict([(invert_dict[k], kwargs[k]) for k in invert_dict])

    if update_dict:

        account = sess.query(User)
        if user_id:
            account = account.filter(
                User.user_id == user_id).update(update_dict)
        elif email:
            account = account.filter(
                User.email == email).update(update_dict)
        else:
            return dict(
                result=0,
                status=2,
                msg=('Missing Argument, '
                     'either "user_id" or "email" should in arguments.'),
                data=None
            )
        result = account
        sess.commit()
        res = dict(result=1, status=0, msg='Successfully', update=result)
    else:
        res = dict(result=0, status=3, msg='Failure')

    return res


TASK_DICT = dict(
    query_account=query_account,
    query_account_by_user_id=query_account_by_user_id,
    query_account_by_flow_id=query_account_by_flow_id,
    insert_account=insert_account,
    insert_account_by_list=insert_account_by_list,
    update_account_expire_time=update_account_expire_time,
    update_account_status=update_account_status,
    update_account_info=update_acount_info)
