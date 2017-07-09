# coding:utf-8
"""Module of Table File Query Function."""

from models import File
from workers.manager import APP as app
from workers.manager import exc_handler


@app.task
@exc_handler
def query_file_by_user_id(user_id, **kwargs):
    """Query file by user ID."""
    sess = kwargs.get('sess')

    file_list = sess.query(File).filter(File.user_id == user_id).all()

    if file_list:
        result = [file.to_dict() for file in file_list]
    else:
        result = None
    return result


@app.task
@exc_handler
def query_file_by_file_id(file_id, **kwargs):
    """Query a file info by file ID."""
    sess = kwargs.get('sess')

    file = sess.query(File).filter(File.file_id == file_id).first()

    if file:
        result = file.to_dict()
        result['file_type'] = result['file_type'].name
    else:
        result = None
    return result


@app.task
@exc_handler
def insert_file(file_id,
                user_id,
                file_name='none.pdf',
                file_size='0',
                valid=1,
                total_pages=0,
                file_type='pdf',
                create_time=0,
                **kwargs):
    """Insert info of a file."""
    sess = kwargs.get('sess')
    new_file = File(
        file_id=file_id,
        user_id=user_id,
        file_name=file_name,
        file_size=file_size,
        valid=valid,
        total_pages=total_pages,
        file_type=file_type,
        create_time=create_time)
    sess.add(new_file)
    sess.commit()

    return dict(result=1, status=0, msg='Successfully')


@app.task
@exc_handler
def update_file_total_pages(file_id, total_pages, **kwargs):
    """Update total pages of a file."""
    sess = kwargs.get('sess')
    file = sess.query(File).filter(File.file_id == file_id).update({
        File.total_pages:
        total_pages
    })
    result = file
    sess.commit()
    return result


TASK_DICT = dict(
    query_file_by_user_id=query_file_by_user_id,
    query_file_by_file_id=query_file_by_file_id,
    insert_file=insert_file,
    update_file_total_pages=update_file_total_pages)
