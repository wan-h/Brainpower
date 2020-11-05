# coding: utf-8
# Author: wanhui0729@gmail.com

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

app = FastAPI()

class LoginIn(BaseModel):
    username: str
    password: str

async def login(item: LoginIn):
    return JSONResponse({
        'name': item.username,
        'pw': item.password
    })

app.add_api_route(methods=['POST'], path='/login', endpoint=login)

if __name__ == '__main__':
    c_client = TestClient(app)
    resp = c_client.post('/login', json={'username': 'test', 'password': '123'})
    print(resp.json())