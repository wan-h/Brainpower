# coding: utf-8
# Author: wanhui0729@gmail.com

'''
tips:
    only work on mac
'''

import os
import requests
import time
from multiprocessing import Value, Pool
from rock.lib.tm import generate_time_str
import socket
import ssl
# pip install PySocks
import socks
# pip install flickrapi
import flickrapi

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()

shareData = Value("i", 0)

'''
flickr图片爬虫
'''

API_KEY = u'e34d3acb7f0a8be138d13acf9a61235a'
API_SECRET = u'2a6649b685f200cb'

def set_socks(ip, port):
    ssl._create_default_https_context = ssl._create_unverified_context
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
    socket.socket = socks.socksocket

class FlickrImageCreeper(object):
    def __init__(self, key=API_KEY, secret=API_SECRET, ip='127.0.0.1', port=1086):
        '''
        Arguments:
            key: flickr key
            secret: flickr secret
            ip: shadowsocks local ip
            port: shadowsocks local port
        '''
        self.key = key
        self.secret = secret
        set_socks(ip, port)

    def _downloadPicture(self, url, output, mannual_time=5, proxies=None):
        try:
            chunk_size = 128
            r = requests.get(url, stream=True, proxies=proxies, verify=False)
            file_name = os.path.join(output, generate_time_str()) + '.jpg'
            with open(file_name, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
            print("\rDownload successfully pics count: {}".format(shareData.value), end='')
            with shareData.get_lock():
                shareData.value += 1
        except Exception as e:
            print("\nDownload fail from {}".format(url))
            print(e)
            time.sleep(mannual_time)

    def _downloadPictures(self, photos, maxNum, output='tmp', mannual_time=5, poolNum=4, proxies=None):
        pool = Pool(poolNum)
        for photo in photos:
            try:
                url = photo.attrib['url_l']
                pool.apply_async(self._downloadPicture, args=(url, output, mannual_time, proxies))
                if maxNum > 0 and shareData.value > maxNum:
                    break
            except:
                pass
        pool.close()
        pool.join()

    # 获取的urls
    def _get_photos(self, keyword):
        flickr = flickrapi.FlickrAPI(self.key, self.secret)
        photos = flickr.walk(tag_mode='all', tags=keyword, extras='url_l')
        return photos

    def crawl(self, keyword, maxNum=10000, output='tmp', poolNum=1):
        '''
        Arguments:
            keyword:爬虫关键字
            maxNum: 爬取数量
            output: 图片输出路径
            poolNum: 开启进程数量
        '''
        photos = self._get_photos(keyword=keyword)
        self._downloadPictures(photos=photos, output=output, poolNum=poolNum, maxNum=maxNum)