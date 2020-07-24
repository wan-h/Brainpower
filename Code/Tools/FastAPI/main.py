# coding: utf-8
# Author: wanhui0729@gmail.com

from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

app = FastAPI()

# 声明请求体
# Field 在 Pydantic 模型内部声明校验
# Config提供文档example
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

class User(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# 构建可选参数值
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 请求体 + 路径参数 + 查询参数
@app.put("/item/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_name": item.name, "item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# 在/item/{item_id}之前，防止被提前解析
@app.get("/items/me")
async def read_user_me():
    return {"item_name": "me", "item_id": 0}

# 多个路径和查询参数
# 可选参数，存在默认值
@app.get("/users/{user_id}/items/{item_id}")
async def read_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# response_model定义输出模型
@app.post("/user/", response_model=UserOut)
async def create_user(user: User):
    return user

# 参数列表，使用定义的enum
@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Query 为查询参数声明更多的校验,定义参数描述
# alias="item-query",表示参数别名，请求可以匹配这个别名赋值给该参数
# deprecated将在文档中说明该参数已弃用，但是接口正常运行
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        deprecated=True
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Path 为路径参数声明相同类型的校验
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results

# 请求体中的单一值body, 直接使用时doc显示不出来
@app.post("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User = Body(...), importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# body嵌入单个请求体参数
# 当只存在一个请求体时其输出会直接映射 Pydantic 模型格式
# {
#   "name": "string",
#   "description": "string",
#   "price": 0,
#   "tax": 0
# }
# body将其保持为单独的请求体参数
# {
#   "item": {
#     "name": "string",
#     "description": "string",
#     "price": 0,
#     "tax": 0
#   }
# }
@app.post("/model/{model_name}")
async def update_item(
    model_name: str, item: Item = Body(..., embed=True)
):
    results = {"item_id": model_name, "item": item}
    return results

"""
运行web服务
uvicorn main:app --reload

服务链接
http://127.0.0.1:8000

交互式文档
http://127.0.0.1:8000/docs

替代文档
http://127.0.0.1:8000/redoc
"""