#!/bin/bash

export LANG=zh_CN.UTF-8

cd ./bin
gunicorn -c ../config/gunicorn.py \
  -k uvicorn.workers.UvicornWorker \
  app:app
