# coding: utf-8
# Author: wanhui0729@gmail.com

import json
import hashlib

def _getTaskId(name):
    md5 = hashlib.md5()
    md5.update(name.encode('utf-8'))
    md5_str = md5.hexdigest()
    return md5_str

def api_create(name, response):
    response.data = {'id': _getTaskId(name)}
    response.ok('Create task successfully.')