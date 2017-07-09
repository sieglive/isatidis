# coding:utf-8
"""PDF interface module.
    This is a dustbin of magic code. If you need, rewrite it by yourself."""
import base64
import os
import platform
import subprocess
from urllib import parse
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from celery import chain, group

from . import (Oss, Tasks, add_label, bindserial, change_ext, config,
               extract_params, figure_id, serial, spam_decode, spam_encode)
from .manager import APP as app

OSS = Oss(endpoint='https://' + config.oss.end_point, bucket=config.oss.bucket)

_PDF_IMAGE_API = os.path.abspath(
    f'core_api/{platform.system()}/PDFImageProcess.exe')


@app.task
@serial
def draw(params_dict, key_in):
    """draw a picture."""
    width, height, text, local_image = extract_params(params_dict, key_in)
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw_worker = ImageDraw.Draw(image)
    font = ImageFont.truetype('templates/font/Raleway-Regular.ttf', 11)
    textw, texth = draw_worker.textsize(text)
    draw_worker.text(
        ((width - textw) / 2, (height - texth) / 2),
        text=text,
        font=font,
        fill='#000000')
    image.save(local_image, 'PNG')
    params_dict.update(dict(width=width, height=height, text=text))
    return params_dict


@app.task
@serial
def download(params_dict, key_in):
    """download a file from OSS"""
    remote_path, local_path = extract_params(params_dict, key_in)
    res = OSS.get(remote_path, local_path)
    if isinstance(res, tuple):
        params_dict['status'] = res[0]
        params_dict['exc_msg'] = res[1]

    return params_dict


@app.task
@serial
def upload(params_dict, key_in):
    """upload a file and delete it."""

    localpath, remotepath, rmfile = extract_params(params_dict, key_in)

    if not os.path.exists(localpath):
        params_dict['status'] = 1
        params_dict['exc_msg'] = 'upload file is not exists.'
        return params_dict
    with open(localpath, 'rb') as file:
        file_stream = file.read()
        params_dict['file_size'] = len(file_stream)
        OSS.put_from_stream(file_stream, remotepath)
    if rmfile:
        os.remove(localpath)

    return params_dict


@app.task
@serial
def count_pages(params_dict, key_in):
    """
    The parameter should be a PDF file's full pathname.
    Return the number of total pages of the given PDF file.

    abs_local_pdf
        - the PDF file's full path name.
    """

    local_pdf, = extract_params(params_dict, key_in)
    abs_local_pdf = os.path.abspath(local_pdf)
    print(abs_local_pdf)
    try:
        out_str = subprocess.check_output([
            _PDF_IMAGE_API,
            '-m',
            'count-pages',
            '-i',
            abs_local_pdf,
        ]).decode('utf-8')
        number_of_total_pages = int(out_str.split('[')[1].split(']')[0])
    except subprocess.CalledProcessError as exception:
        params_dict['status'] = exception.returncode
        if params_dict['status'] == 0:
            params_dict['exc_msg'] = 'Nothing wrong. Not suppose to happen.'
        elif params_dict['status'] == 1:
            params_dict['exc_msg'] = 'Wrong parameter. Not suppose to happen.'
        elif params_dict['status'] == 2:
            params_dict['exc_msg'] = 'Need password.'
        elif params_dict['status'] == 3:
            params_dict['exc_msg'] = 'Broken PDF.'
        elif params_dict['status'] == 4:
            params_dict['exc_msg'] = 'Broken PDFImageProcess.exe.'
        else:
            params_dict['exc_msg'] = 'Unknown Error.'
        number_of_total_pages = 0

    if 'key_out' in params_dict:
        key_list = params_dict.get('key_out')
        params_dict[key_list[0]] = number_of_total_pages

    return params_dict


@app.task
@serial
def convert_pdf_to_image(params_dict, key_in):
    """Convert a page of PDF file to image.
    exit_code 0: Success
    exit_code 1: Parameters error
    exit_code 2: Need password
    exit_code 3: Broken file
    exit_code 4: Program crashed(eg. file not exists)
    """
    local_path, page_num, remote_pdf = extract_params(params_dict, key_in)
    dpi = '144'
    if 'dpi' in params_dict:
        dpi = params_dict.get('dpi')

    abs_local_pdf = os.path.abspath(local_path)
    image_path = change_ext(abs_local_pdf, '.jpg')
    abs_local_image = add_label(image_path, f'/{ page_num }')

    if not os.path.exists(local_path):
        params_dict['status'] = 4
        params_dict['exc_page_num'] = page_num
        params_dict['exc_msg'] = 'File not exists.'
        return params_dict

    try:
        subprocess.check_output([
            _PDF_IMAGE_API,
            '-m',
            'to-image',
            '-p',
            f'{ page_num - 1 }',
            '-i',
            abs_local_pdf,
            '-o',
            abs_local_image,
            '-d',
            dpi,
        ])
    except subprocess.CalledProcessError as exception:
        params_dict['status'] = exception.returncode
        params_dict['exc_page_num'] = page_num
        params_dict['exc_msg'] = 'Program error.'
        return params_dict
    if 'abs_local_image' in params_dict:
        raise ValueError('Key \'abs_local_image\' is already in params.')
    if 'key_out' in params_dict:
        key_list = params_dict.get('key_out')
        remote_image = change_ext(
            add_label(remote_pdf, f'/{ page_num }'), '.jpg')
        params_dict[key_list[0]] = abs_local_image
        params_dict[key_list[1]] = remote_image
    return params_dict


@app.task(bind=True)
@bindserial
def convert_pdf_to_images(self, params_dict, key_in):
    """Convert specified page of PDF file to images."""
    pdf_path, pages, token, top = extract_params(params_dict, key_in)

    # local_path = os.path.basename(pdf_path)
    # token = figure_id()
    local_path = 'files/' + token + '.pdf'
    if os.path.exists(local_path) and top:
        params_dict['status'] = 4
        params_dict['exc_msg'] = f'{ local_path } is converting.'
        return params_dict

    params = {
        'status': 0,
        'file_id': change_ext(os.path.basename(pdf_path), ''),
        'rand_id': token,
        'local_pdf': local_path,
        'origin_pdf': pdf_path
    }
    params = spam_encode(params)
    download_key_in = ['origin_pdf', 'local_pdf']
    convert_key_in = ['local_pdf', 'page_num', 'origin_pdf']
    convert_key_out = ['abs_local_image', 'remote_image']
    upload_key_in = ['abs_local_image', 'remote_image', 'rmfile']

    try:
        os.mkdir('files/' + token)
    except FileExistsError:
        pass
    print(top)

    download_mission = download.s(params, download_key_in)
    dl_params = download_mission.apply_async().get()

    if pages == 'all':
        count_key_in = ['local_pdf']
        count_key_out = ['pages']
        count_mission = count_pages.s(
            dl_params, count_key_in, key_out=count_key_out).apply_async()
        ct_params = count_mission.get()
        print(ct_params)
        if int(ct_params[:2], 16) == 0:
            total_pages = spam_decode(ct_params)['pages']
            pages = list(range(1, total_pages + 1))
            params_dict['total_pages'] = total_pages
            print(params_dict)
        else:
            pages = [0]

    if top:
        group_mission = group(
            chain(
                convert_pdf_to_image.s(
                    dl_params,
                    convert_key_in,
                    page_num=page_num,
                    key_out=convert_key_out),
                upload.s(upload_key_in, rmfile=True))
            for page_num in pages[:3]).apply_async()

        convert_args = {
            'status': 0,
            'remote_path': pdf_path,
            'pages': pages[3:],
            'token': token,
            'top': False
        }
        print(convert_args)
        key_in = ['remote_path', 'pages', 'token', 'top']
        encode_args = spam_encode(convert_args)
        tasks = group_mission.get()
        self.apply_async(args=[encode_args, key_in])

    else:
        group_mission = group(
            chain(
                convert_pdf_to_image.s(
                    dl_params,
                    convert_key_in,
                    page_num=page_num,
                    key_out=convert_key_out),
                upload.s(upload_key_in, rmfile=True))
            for page_num in pages).apply_async()
        tasks = group_mission.get()
        try:
            os.remove(local_path)
            os.rmdir('files/' + token)
        except FileNotFoundError:
            pass
        except OSError as exception:
            print('\n' * 10)
            print(os.listdir('files/' + token))
            print('\n' * 10)
            raise exception

    decoded_tasks = [spam_decode(task) for task in tasks]
    fail_task = [
        task['exc_page_num'] for task in decoded_tasks
        if 'exc_page_num' in task
    ]
    params_dict['fail_task'] = fail_task
    return params_dict


@app.task
@serial
def remove_bg(params_dict, key_in):
    """
    The parameter should be an image file's full pathname.
    Remove the background of the target image and return
    the filename of the new image.

    abs_local_sign
        - the PDF file's full path name.
    """
    local_sign, = extract_params(params_dict, key_in)
    abs_local_sign = os.path.abspath(local_sign)
    # path = os.path.dirname(abs_local_sign)

    try:
        subprocess.check_output([
            _PDF_IMAGE_API,
            '-m',
            'remove-background',
            '-i',
            abs_local_sign,
            '-o',
            abs_local_sign + '.rb',
        ]).decode('utf-8')
    except subprocess.CalledProcessError as exception:
        params_dict['status'] = exception.returncode
        if exception.returncode == 1:
            params_dict['exc_msg'] = 'Wrong parameter. Not suppose to happen.'
        elif exception.returncode == 3:
            params_dict['exc_msg'] = 'Broken image.'
        elif exception.returncode == 4:
            params_dict['exc_msg'] = 'Broken PDFImageProcess.exe'
        else:
            params_dict['exc_msg'] = 'Unknown error.'

    os.remove(abs_local_sign)
    os.rename(abs_local_sign + '.rb', abs_local_sign)
    return params_dict


@app.task
@serial
def remove_bg_and_upload(params_dict, key_in):
    """
    The parameter should be an image file's full pathname.
    Remove the background of the target image and return the filename of the
    new image.

    abs_local_sign
        - the PDF file's full path name.
    """
    remote_path, sign_data = extract_params(params_dict, key_in)
    token = figure_id()
    local_sign = token + '.png'

    # path = os.path.dirname(abs_local_sign)

    with open(local_sign, 'wb') as image:
        data = base64.b64decode(sign_data.encode('utf-8'))
        image.write(data)

    params = {
        'status': 0,
        'rand_id': token,
        'remote_sign': remote_path,
        'local_sign': local_sign,
    }
    params = spam_encode(params)
    remove_bg_key_in = ['local_sign']
    upload_key_in = ['local_sign', 'remote_sign', 'rmfile']

    remove_bg_mission = remove_bg.s(params, remove_bg_key_in)
    rb_params = remove_bg_mission.apply_async(args=[], retry=False).get()

    upload_mission = upload.s(rb_params, upload_key_in, rmfile=True)
    up_params = upload_mission.apply_async(args=[], retry=False).get()

    return spam_decode(up_params)


@app.task
@serial
def add_image_to_pdf(params_dict, key_in):
    """
    Add an image of a signature to the PDF file.
    Return the PDF file's full pathname.

    PARAMETER
        abs_local_pdf
            - the PDF file's full path name.
        abs_local_sign
            - the signature image's full path name. The image should be a png.
        pos_x
            - relative x coordinate reference to the two file's left-bottom
              corner.
        pos_y
            - relative y coordinate reference to the two file's left-bottom
              corner.
        img_w
            - the width of the image you want to display.
        img_h
            - the height of the image you want to display.
        page_number
            - the page where you want to sign.
    """

    local_pdf, local_sign, sign_data = extract_params(params_dict, key_in)

    try:
        pos_x = str(round(sign_data['pos_x']))
        pos_y = str(round(sign_data['pos_y']))
        img_w = str(round(sign_data['img_w']))
        img_h = str(round(sign_data['img_h']))
        page = str(sign_data['page'])
    except KeyError as exception:
        params_dict['status'] = 5
        key = exception.args[0]
        params_dict['exc_msg'] = f'Sign data should have key "{ key }" in it'
        return params_dict

    abs_local_pdf = os.path.abspath(local_pdf)
    abs_local_sign = os.path.abspath(local_sign)

    page = str(page)

    ooo = [
        _PDF_IMAGE_API,
        '-m',
        'add-image',
        '-i',
        abs_local_sign,
        '-o',
        abs_local_pdf,
        '-x',
        pos_x,
        '-y',
        pos_y,
        '-w',
        img_w,
        '-h',
        img_h,
        '-p',
        page,
    ]
    print(' '.join(ooo))
    try:
        subprocess.check_output(ooo).decode('utf-8')
    except subprocess.CalledProcessError as exception:
        print(exception)
        params_dict['status'] = exception.returncode
        if params_dict['status'] == 1:
            params_dict['exc_msg'] = 'Wrong parameter. Not suppose to happen.'
        elif params_dict['status'] == 3:
            params_dict['exc_msg'] = 'Broken PDF.'
        elif params_dict['status'] == 4:
            params_dict['exc_msg'] = 'Broken PDFImageProcess.exe'
        else:
            params_dict['exc_msg'] = 'Unknown Error'

    return params_dict


@app.task
@serial
def add_images_to_pdf(params_dict, key_in):
    """Add images to pdf."""
    path, flow_info, image_data_list, filename = extract_params(
        params_dict, key_in)

    remote_path, new_remote_path = path

    token = figure_id()
    local_path = f'files/{token}.pdf'

    if os.path.exists(local_path):
        params_dict['status'] = 4
        params_dict['exc_msg'] = f'{ local_path } is converting.'
        return params_dict

    params_dict = {
        'status': 0,
        'file_id': change_ext(os.path.basename(remote_path), ''),
        'rand_id': token,
        'local_pdf': local_path,
        'origin_pdf': remote_path,
        'new_remote_path': new_remote_path,
        'data_list': image_data_list
    }
    encode_params = spam_encode(params_dict)
    download_key_in = ['origin_pdf', 'local_pdf']
    # download_sign_key_in = ['remote_image', 'local_image']
    merge_key_in = ['local_pdf', 'local_image', 'sign_data']

    download_mission = download.s(encode_params, download_key_in)
    dl_params = download_mission.apply_async().get()
    mg_params = dl_params

    # group_download = group(
    #     download.s(
    #         spam_encode(
    #             dict(params_dict, **dict(
    #                 remote_image=image['remote_image'],
    #                 local_image=f'{token}-{i}.png'
    #             ))),
    #         download_sign_key_in,
    #         task_num=i) for (i, image) in enumerate(image_data_list))
    # tasks = group_download.apply_async().get()

    # fail_tasks = [res['task_num'] for res in tasks if int(res[:2], 16) != 0]

    for i, image_data in enumerate(image_data_list):
        file_id = flow_info.get('file_id')
        page_num = image_data.get('page')
        page_w, page_h = OSS.get_size(f'files/{file_id}/{page_num}.jpg')

        page_w /= 2.0
        page_h /= 2.0
        print(page_w, page_h)
        react_x = page_w * image_data['pos_x']
        react_y = page_h * image_data['pos_y']
        react_w = page_w * image_data['pos_w']
        react_h = page_h * image_data['pos_h']
        time.sleep(1)
        local_image = f'files/{token}-{i}.png'
        print('=============> ', image_data['sign_type'])
        if image_data['sign_type'] == 'image':
            dl_mission = download.s(spam_encode(
                dict(params_dict, **dict(
                    remote_image=parse.urlparse(image_data['content']).path[1:],
                    local_image=local_image
                ))), ['remote_image', 'local_image'])
            dl_mission.apply_async().get()
        elif image_data['sign_type'] == 'text':
            draw_mission = draw.s(spam_encode(
                dict(params_dict, **dict(
                    width=int(react_w),
                    height=int(react_h),
                    text=image_data['content'],
                    local_image=local_image
                ))), ['width', 'height', 'text', 'local_image'])
            draw_mission.apply_async().get()
        else:
            print('Unknown Image Type:', image_data['sign_type'])
            continue

        image = Image.open(os.getcwd() + '/' + local_image)
        img_w, img_h = image.size
        image.close()

        img_rate = img_w / img_h
        react_rate = react_w / react_h

        if img_rate > react_rate:
            cvt_w = react_w
            cvt_h = img_h * react_w / img_w
            delta_w = 0
            delta_h = (react_h - cvt_h) / 2
        else:
            cvt_h = react_h
            cvt_w = img_w * react_h / img_h
            delta_w = (react_w - cvt_w) / 2
            delta_h = 0

        data = dict(
            pos_x=react_x + delta_w,
            pos_y=page_h - react_y - react_h + delta_h,
            img_w=cvt_w,
            img_h=cvt_h,
            page=page_num - 1 if page_num > 0 else page_num)

        params_dict = spam_decode(mg_params)
        params_dict['local_image'] = local_image
        params_dict['sign_data'] = data
        for key in params_dict:
            print(f'{key}: {params_dict[key]}')
        mg_params = spam_encode(params_dict)
        merge_mission = add_image_to_pdf.s(mg_params, merge_key_in)
        mg_params = merge_mission.apply_async().get()

        os.remove(local_image)

        params_dict = spam_decode(mg_params)
        if params_dict.get('status') is not 0:
            params_dict['exc_num'] = i + 1
            return spam_encode(params_dict)

    params_dict = spam_decode(dl_params)
    # params_dict['fail_tasks'] = fail_tasks

    upload_key_in = ['local_pdf', 'new_remote_path', 'rmfile']
    upload_mission = upload.s(
        dl_params, upload_key_in, rmfile=True).apply_async()
    up_params = upload_mission.get()

    OSS.set_filename(new_remote_path, filename)

    return spam_decode(up_params)


TASKS = Tasks(
    dict(
        convert_pdf_to_images=convert_pdf_to_images,
        add_images_to_pdf=add_images_to_pdf,
        remove_bg_and_upload=remove_bg_and_upload))


