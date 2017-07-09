# coding:utf-8
"""Module of payment query function."""
import time

from models import m_client
from workers.manager import APP as app
from workers.task_database import TASKS as db_tasks

SESSION = m_client.session

@app.task
def payment_task(cart_callback_data, **_kwargs):
    """The top handler of payment callback request."""
    info = dict(now=time.time())
    db_user_info = db_tasks.query_account.apply_async(
        args=[cart_callback_data['email']]).get()

    if not db_user_info:
        return dict(result=0, status=1, msg='Account not exist.')

    info['basic_time'] = db_user_info['expire_time']

    if info['basic_time'] > info['now']:
        info['expire_time'] = info['basic_time']
    else:
        info['expire_time'] = info['now']

    sess = m_client.payment_record
    payment = sess.find_one({'order_num': cart_callback_data['order_num']})

    if payment is None:
        sess.insert_one(cart_callback_data)
        prods = cart_callback_data['product_list']
        for prod in prods:
            if prods[prod]['license_id'] == '60':
                info['expire_time'] += 31104000 * int(prods[prod]['quantity'])
            elif prods[prod]['license_id'] == '125':
                info['expire_time'] += 2592000 * int(prods[prod]['quantity'])

        db_tasks.update_account_expire_time.apply_async(
            args=[cart_callback_data['email'], info['expire_time']]).get()

    elif not payment['external_customer_reference']:
        sess.update_one(
            dict(order_num=cart_callback_data['order_num']), {
                '$set':
                dict(external_customer_reference=cart_callback_data[
                    'external_customer_reference'])
            })

    return dict(
        result=1,
        status=0,
        data=info,
        msg='Deal with cart callback data successfully.')
