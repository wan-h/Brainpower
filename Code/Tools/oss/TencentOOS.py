# coding: utf-8
# Author: wanhui0729@gmail.com

'''
Tencent OSS
模块安装
pip install -U cos-python-sdk-v5
'''

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
import os
import sys
import logging

class OSSManager(object):
    def __init__(self, region, secret_id, secret_key, token=None, scheme=None, logger_name=None):
        '''
        :param region:用户的 Region
        :param secret_id:用户的 secretId
        :param secret_key:用户的 secretKey
        :param token:使用临时密钥需要传入 Token，默认为空，可不填
        :param scheme:指定使用 http/https 协议来访问 COS，默认为 https，可不填
        '''
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        self.client = CosS3Client(config)
        if logger_name is not None:
            self.logger = logging.getLogger(logger_name)
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            self.logger = logging.getLogger()

    def creat_bucket(self, bucket):
        '''创建存储桶'''
        response = self.client.create_bucket(Bucket=bucket)
        self.logger.info("creat bucket: {}".format(bucket))
        return response

    def delete_bucket(self, bucket):
        '''删除存储桶'''
        response = self.client.delete_bucket(Bucket=bucket)
        self.logger.info("delete bucket: {}".format(bucket))
        return response

    def list_buckets(self):
        '''查询存储桶列表'''
        response = self.client.list_buckets()
        return response

    def put_object(self, bucket, key, file, enableMD5=False, style='simple'):
        '''
        upload object
        :param bucket: bucket
        :param file: local path
        :param key: oss path
        :param enableMD5: bool
        :param style: 1.simple(简单上传接口) 2.advance(高级上传接口,支持断点续传)
        '''
        if style not in ['simple', 'advance']:
            raise Exception("Please sure upload style must in ['simple', 'advance']")
        if not os.path.exists(file):
            raise Exception("Please sure file exits.")

        if style == 'simple':
            with open(file, 'rb') as fp:
                response = self.client.put_object(
                    Bucket=bucket,
                    Body=fp,
                    Key=key,
                    StorageClass='STANDARD',
                    EnableMD5=enableMD5
                )
        elif style == 'advance':
            response = self.client.upload_file(
                Bucket=bucket,
                LocalFilePath=file,
                Key=key,
                PartSize=1,
                MAXThread=10,
                EnableMD5=enableMD5
            )
        self.logger.info("PUT object to {}/{}".format(bucket, key))
        return response['ETag']

    def get_object(self, bucket, key, style='file', file=None):
        '''
        download object
        :param bucket: bucket
        :param file: local path
        :param key: oss path
        :param style: 1.file(下载文件到本地) 2.stream(下载文件流)
        '''
        if style not in ['file', 'stream']:
            raise Exception("Please sure download style must in [ 'file', 'stream' ]")
        if style == 'file' and file is None:
                raise Exception("Please sure local file address.")
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
        except CosServiceError as e:
            self.logger.error(e.get_origin_msg())
            self.logger.error(e.get_digest_msg())
            self.logger.error(e.get_status_code())
            self.logger.error(e.get_error_code())
            self.logger.error(e.get_error_msg())
            self.logger.error(e.get_resource_location())
            self.logger.error(e.get_trace_id())
            self.logger.error(e.get_request_id())
            raise Exception("CosServiceError")

        self.logger.info("GET object from {}/{}".format(bucket, key))

        if style == 'file':
            # return file address
            response['Body'].get_stream_to_file(file)
            return file
        elif style == 'stream':
            # return data stream
            fp = response['Body'].get_raw_stream()
            return fp

    def delete_object(self, bucket, keys):
        '''
        delete object
        :param bucket: bucket
        :param keys: a list of oss path
        :return:
        '''
        Delete = {
            'Object': [],
            'Quiet': 'false'
        }

        for key in keys:
            key_dict = {'key': key}
            Delete['Object'].append(key_dict)
            self.logger.info("DELETE object from {}/{}".format(bucket, key))

        response = self.client.delete_objects(Bucket=bucket, Delete=Delete)
        return response