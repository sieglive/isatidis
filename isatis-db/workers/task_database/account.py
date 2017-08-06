# coding: utf-8

from models import Account
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_account_by_user_id(user_id, **kwargs):
    """Query account"""
    sess = kwargs.get('sess')
    account = sess.query(
        Account).filter(Account.user_id == user_id).first()

    if account:
        result = account.to_dict()
    else:
        result = None
    return result


@app.task
@exc_handler
def insert_account(user_name,
                   nick_name,
                   user_pass,
                   email,
                   appear_time,
                   register_time,
                   permission=0,
                   avatar_path='',
                   active_status=0,
                   valid=1,
                   expire_time=0,
                   **kwargs):
    """Insert an account."""
    sess = kwargs.get('sess')
    new_account = Account(
        user_name=user_name,
        nick_name=nick_name,
        user_pass=user_pass,
        email=email,
        permission=permission,
        avatar_path=avatar_path,
        active_status=active_status,
        valid=valid,
        appear_time=appear_time,
        register_time=register_time,
        expire_time=expire_time,
    )
    sess.add(new_account)
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


TASK_DICT = dict(
    query_account_by_user_id=query_account_by_user_id,
    insert_account=insert_account)
