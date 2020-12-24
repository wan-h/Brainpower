# coding: utf-8
# Author: wanhui0729@gmail.com

'''
Amason OSS
模块安装
pip install boto3
'''

import os
import sys
from boto3 import Session
import logging

class OSSManager(object):
    def __init__(self, url, secret_id, secret_key, token=None, region=None, logger_name=None):
        '''
        :param url:host地址
        :param secret_id:用户的 secretId
        :param secret_key:用户的 secretKey
        :param token:使用临时密钥需要传入 Token，默认为空，可不填
        :param scheme:指定使用 http/https 协议来访问 COS，默认为 https，可不填
        '''
        session = Session(
            aws_access_key_id=secret_id,
            aws_secret_access_key=secret_key,
            aws_session_token=token,
            region_name=region
        )
        self.client = session.client('s3', endpoint_url=url)
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
        for bucket in response['Buckets']:
            self.logger.info("{name}\t{created}".format(
                name=bucket['Name'],
                created=bucket['CreationDate']
            ))
        return response

    def put_object(self, bucket, key, file, style='simple'):
        '''
        upload object
        :param bucket: bucket
        :param file: local path
        :param key: oss path
        '''
        if style not in ['simple', 'advance']:
            raise Exception("Please sure upload style must in ['simple', 'advance']")
        if not os.path.exists(file):
            raise Exception("Please sure file exits.")
        if style == 'simple':
            with open(file, 'rb') as fp:
                response = self.client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=fp
                )
        elif style == 'advance':
            response = self.client.upload_file(
                Bucket=bucket,
                Filename=file,
                Key=key,
            )
        self.logger.info("PUT object to {}/{}".format(bucket, key))
        return response

    def get_object(self, bucket, key, style='file', file=None):
        '''
        get object
        :param bucket: bucket
        :param key: oss path
        '''
        if style not in ['file', 'stream']:
            raise Exception("Please sure download style must in [ 'file', 'stream' ]")
        if style == 'file' and file is None:
            raise Exception("PPlease sure local file address.")
        try:
            if style == 'stream':
                response = self.client.get_object(Bucket=bucket, Key=key)
                fp = response['Body'].get_raw_stream()
            elif style == 'file':
                self.client.download_file(
                    Bucket=bucket,
                    Key=key,
                    Filename=file
                )
                fp = file

        except Exception as e:
            self.logger.error(e)
            raise Exception("S3ServiceError")
        self.logger.info("GET object from {}/{}".format(bucket, key))
        return fp

    def delete_object(self, bucket, keys):
        '''
        delete object
        :param bucket: bucket
        :param keys: a list of oss path
        :return:
        '''
        Delete = {
            'Objects': [],
            'Quiet': False
        }

        for key in keys:
            key_dict = {'Key': key}
            Delete['Objects'].append(key_dict)
            self.logger.info("DELETE object from {}/{}".format(bucket, key))

        response = self.client.delete_objects(Bucket=bucket, Delete=Delete)
        return response
