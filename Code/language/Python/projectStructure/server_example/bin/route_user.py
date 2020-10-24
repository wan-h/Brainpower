# coding: utf-8
# Author: wanhui0729@gmail.com

import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.server.response import Response
from lib.server import server_user

userRouter = APIRouter()

class BaseOutItems(BaseModel):
    message: str
    code: int

class UserIn(BaseModel):
    name: str
    phone: str

class UserID(BaseModel):
    id: str

class UserOut(BaseOutItems):
    data: UserID

@userRouter.post('/v0/register/', response_model=UserOut)
async def api_register(item: UserIn):
    response = Response()
    params = json.loads(item.json())
    name = params['name']
    phone = params['phone']
    server_user.api_register(name, phone, response)
    # 校验返回数据结构的字段: 多余字段会被踢出, 缺少字段会报异常
    resp_json = response.validate_response(UserOut)
    return JSONResponse(status_code=200, content=resp_json)