# coding: utf-8
# Author: wanhui0729@gmail.com

import requests
if __name__ == '__main__':
    url = "http://localhost:5000/hello/"
    response = requests.post(url=url, data="hello world")
    print(response.text)