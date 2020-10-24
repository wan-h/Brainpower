# coding: utf-8
# Author: wanhui0729@gmail.com

import os, sys
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

import uvicorn
from fastapi import FastAPI
from bin.route_user import userRouter
from bin.route_task import taskRouter

app = FastAPI(
    title="Server Example",
    description="This is my server example.",
    version="1.0.0",
)

# 路由
app.include_router(userRouter, prefix="/user")
app.include_router(taskRouter, prefix='/task')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000, access_log=True)