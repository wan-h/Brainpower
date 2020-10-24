# coding: utf-8
# Author: wanhui0729@gmail.com

import json
import hashlib

def _getUserId(name, phone):
    md5 = hashlib.md5()
    md5.update((name + phone).encode('utf-8'))
    md5_str = md5.hexdigest()
    return md5_str

def api_register(name, phone, response):
    response.data = {'id': _getUserId(name, phone)}
    response.ok('Get user ID successfully.')