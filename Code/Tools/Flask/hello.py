# coding: utf-8
# Author: wanhui0729@gmail.com

from flask import Flask, request

app = Flask(__name__)

@app.route('/hello/', methods=['POST'])
def hello_word():
    data = request.data
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

