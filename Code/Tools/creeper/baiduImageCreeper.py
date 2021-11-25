# coding: utf-8
# Author: wanhui0729@gmail.com

import os
import re
import requests
import time
from multiprocessing import Value, Pool
from rock.lib.tm import generate_time_str

shareData = Value("i", 0)

'''
百度图片爬虫
'''
class BaiduImageCreeper(object):
    def __init__(self):
        self.pageCount = 0
        self.urlCount = 0
        # self.picCount = 0

    def _downloadPicture(self, url, output, mannual_time=5):
        try:
            pic = requests.get(url, timeout=15)
            file_name = os.path.join(output, generate_time_str()) + '.jpg'
            with open(file_name, 'wb') as f:
                f.write(pic.content)
            print("\rDownload successfully from page {} , pics count: {}".format(self.pageCount, shareData.value), end='')
            with shareData.get_lock():
                shareData.value += 1
        except Exception as e:
            print("\nDownload fail from {}".format(url))
            print(e)
            time.sleep(mannual_time)

    # def _downloadPictures(self, urls, output, mannual_time=5):
    #     if not isinstance(urls, (list, tuple)):
    #         urls = list(urls)
    #     for url in urls:
    #         try:
    #             pic = requests.get(url, timeout=15)
    #             file_name = os.path.join(output, generate_time_str()) + '.jpg'
    #             with open(file_name, 'wb') as f:
    #                 f.write(pic.content)
    #             print("\rDownload successfully from page {} , pics count: {}".format(self.pageCount, self.picCount), end='')
    #             self.picCount += 1
    #         except Exception as e:
    #             print("\nDownload fail from {}".format(url))
    #             print(e)
    #             time.sleep(mannual_time)
    #             continue
    def _downloadPictures(self, urls, output='tmp', mannual_time=5, poolNum=4):
        if not isinstance(urls, (list, tuple)):
            urls = list(urls)
        pool = Pool(poolNum)
        for url in urls:
            pool.apply_async(self._downloadPicture, args=(url, output, mannual_time))
        pool.close()
        pool.join()

    # 获取单个翻页的所有图片的urls+当前翻页的下一翻页的url
    def _get_onepage_urls(self, onepageurl):
        if not onepageurl:
            print('The last Page!')
            return [], ''
        try:
            html = requests.get(onepageurl).text
        except Exception as e:
            print(e)
            pic_urls = []
            fanye_url = ''
            return pic_urls, fanye_url
        self.pageCount += 1
        pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
        self.urlCount += len(pic_urls)
        nextPageUrls = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
        nextPageUrl = 'http://image.baidu.com' + nextPageUrls[0] if nextPageUrls else ''
        return pic_urls, nextPageUrl

    def crawl(self, keyword, maxNum=-1, output='tmp', poolNum=1):
        '''
        Arguments:
            keyword:爬虫关键字
            maxNum: 爬取数量
            output: 图片输出路径
            poolNum: 开启进程数量
        '''
        url_init_first = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn=0&gsm=0x0&ct=&ic=0&lm=-1&width=0&height=0"
        page_url = url_init_first.format(keyword)
        while True:
            pic_urls, page_url = self._get_onepage_urls(page_url)
            self._downloadPictures(pic_urls, output, poolNum)
            print("\t Pages: {} | Urls: {} | Pics: {}".format(self.pageCount, self.urlCount, shareData.value))
            if maxNum > 0 and shareData.value >= maxNum or page_url == '':
                break