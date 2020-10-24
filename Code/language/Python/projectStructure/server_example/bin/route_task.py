# coding: utf-8
# Author: wanhui0729@gmail.com

import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.server.response import Response
from lib.server import server_task

taskRouter = APIRouter()

class BaseOutItems(BaseModel):
    message: str
    code: int

class TaskIn(BaseModel):
    name: str

class TaskID(BaseModel):
    id: str

class TaskOut(BaseOutItems):
    data: TaskID

@taskRouter.post('/v0/create/', response_model=TaskOut)
async def api_register(item: TaskIn):
    response = Response()
    params = json.loads(item.json())
    name = params['name']
    server_task.api_create(name, response)
    # 校验返回数据结构的字段: 多余字段会被踢出, 缺少字段会报异常
    resp_json = response.validate_response(TaskOut)
    return JSONResponse(status_code=200, content=resp_json)