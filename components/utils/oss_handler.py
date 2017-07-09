# -*- coding:utf-8 -*-
"""OSSHandler module"""
import oss2

from utils import config


class Oss:
    """Class to handle OSS api"""

    def __init__(self,
                 endpoint,
                 bucket,
                 key_id=config.oss.access_key,
                 key_secret=config.oss.access_key_secret):
        self.key_id = key_id
        self.key_secret = key_secret
        self.endpoint = endpoint  # 'http://oss-cn-shenzhen.aliyuncs.com'
        self.bucket = bucket  # 'sz-pe-pdf-test'
        self.auth = oss2.Auth(self.key_id, self.key_secret)
        self.handler = oss2.Bucket(self.auth, self.endpoint, self.bucket)

    def get(self, remote_path, local_path):
        """get file from OSS"""
        try:
            self.handler.get_object_to_file(remote_path, local_path)
            return local_path
        except oss2.exceptions.RequestError:
            return (6, 'OSS get {} failed.'.format(remote_path))
        except oss2.exceptions.NoSuchKey as exceptions:
            return (6, 'OSS file is not exist. ===> ' + str(exceptions))

    def put(self, local_path, remote_path=None):
        """put file to OSS"""
        try:
            self.handler.put_object_from_file(remote_path, local_path)
            return remote_path
        except oss2.exceptions.RequestError:
            print('fail to upload {}'.format(remote_path))
            return False

    def get_to_stream(self, remote_path):
        """get file from OSS"""
        try:
            local_stream = self.handler.get_object(remote_path)
            return local_stream
        except oss2.exceptions.RequestError:
            return (0, 'OSS get {} failed.'.format(remote_path))
        except oss2.exceptions.NoSuchKey as exceptions:
            return (0, 'OSS file is not exist. ===>' + str(exceptions))

    def put_from_stream(self, local_stream, remote_path=None):
        """put file to OSS"""
        try:
            self.handler.put_object(remote_path, local_stream)
            return remote_path
        except oss2.exceptions.RequestError:
            return (0, 'put file to {} on OSS failed.'.format(remote_path))

    def delete(self, remote_path):
        """delete file from OSS"""
        try:
            self.handler.delete_object(remote_path)
            return True
        except oss2.exceptions.RequestError:
            print('fail to delete {}'.format(remote_path))
            return False

    def set_filename(self, remote_path, filename):
        """Set download name of a file."""
        try:
            self.handler.update_object_meta(
                remote_path,
                {'Content-Disposition': f'attachment;filename="{filename}"'})
            return True
        except oss2.exceptions.RequestError:
            print(f'fail to update filename of {remote_path}')
            return False

    def get_path(self, path):
        """assemble full url of the object path"""
        return 'https://{}.{}/{}'.format(
            self.bucket, config.oss.end_point, path)

    def object_exists(self, path):
        """check the path exists or not"""
        return self.handler.object_exists(path)

    def get_size(self, path):
        """get size of image."""
        remote_stream = self.handler.get_object(path, byte_range=(0, 170))
        bstr = remote_stream.read()

        if bstr[:4] == b'\x89PNG':
            # PNG
            width = 0
            width = width * 256 + bstr[18]
            width = width * 256 + bstr[19]
            height = 0
            height = height * 256 + bstr[22]
            height = height * 256 + bstr[23]
        elif bstr[:2] == b'\xff\xd8':
            # JPEG
            height = bstr[163] * 256 + bstr[164]
            width = bstr[165] * 256 + bstr[166]
        else:
            width = 0
            height = 0

        return (width, height)
