# coding:utf-8
"""Test celery module."""
import base64
import os
import sys
import time

from workers.task_convert import (add_images_to_pdf, convert_pdf_to_images,
                                  remove_bg_and_upload)

from . import spam_decode, spam_encode


def test_convert_pdf_to_image():
    """test"""
    args = {
        'status': 0,
        'remote_path': sys.argv[2],
        'pages': [1, 2, 3, 10, 50, 1000],
        'token': '0000-b18c-15c0-6ddd-e83'
    }
    key_in = ['remote_path', 'pages', 'token']
    encode_args = spam_encode(args)
    res = convert_pdf_to_images.apply_async(args=[encode_args, key_in])
    print(res.result)
    print(spam_decode(res.get()))


def test_remove_bg_and_upload():
    """test"""
    with open('asd.png', 'rb') as image:
        image_data = image.read()
    bs64_data = base64.b64encode(image_data).decode('utf-8')

    args = {'status': 0, 'remote_path': sys.argv[2], 'data': bs64_data}
    key_in = ['remote_path', 'data']
    encode_args = spam_encode(args)
    res = remove_bg_and_upload.apply_async(args=[encode_args, key_in])
    print(spam_decode(res.get()))


def test_add_images_to_pdf():
    """test"""
    image_list = [
        {
            'pos_x': 100,
            'pos_y': 200,
            'img_w': 400,
            'img_h': 200,
            'page': 2,
            'remote_image': 'test1.png'
        },
        {
            'pos_x': 100,
            'pos_y': 200,
            'img_w': 400,
            'img_h': 200,
            'page': 3,
            'remote_image': 'test1.png'
        },
        {
            'pos_x': 100,
            'pos_y': 200,
            'img_w': 400,
            'img_h': 200,
            'page': 4,
            'remote_image': 'test1.png'
        },
        {
            'pos_x': 100,
            'pos_y': 200,
            'img_w': 400,
            'img_h': 200,
            'page': 5,
            'remote_image': 'test1.png'
        },
        {
            'pos_x': 100,
            'pos_y': 200,
            'img_w': 400,
            'img_h': 200,
            'page': 6,
            'remote_image': 'test1.png'
        },
    ]
    args = {
        'status': 0,
        'remote_path': sys.argv[2],
        'new_path': sys.argv[3],
        'image_data_list': image_list
    }
    key_in = ['remote_path', 'new_path', 'image_data_list']

    encode_args = spam_encode(args)
    res = add_images_to_pdf.apply_async(args=[encode_args, key_in])
    print(spam_decode(res.get()))


if __name__ == '__main__':
    # python3 test_celery.py 3 files/test.pdf files/test_merge.pdf
    # python3 test_celery.py 2 test.png
    # python3 test_celery.py 1 files/test.pdf
    print('-' * 20)
    print(os.getcwd())
    print()
    A = time.time()
    if sys.argv[1] == '1':
        test_convert_pdf_to_image()
    elif sys.argv[1] == '2':
        test_remove_bg_and_upload()
    elif sys.argv[1] == '3':
        test_add_images_to_pdf()
    else:
        print('Unknown argument "%s".' % sys.argv[1])
    B = time.time() - A
    print('-' * 20)
    print('Mission completed in %.3f sec.' % B)
