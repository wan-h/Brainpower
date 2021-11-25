# coding: utf-8
# Author: wanhui0729@gmail.com

from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
# 前后端分离，解决前端报跨域的问题
CORS(app)

@app.route('/hello/', methods=['POST'])
def hello_word():
    data = request.data
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

