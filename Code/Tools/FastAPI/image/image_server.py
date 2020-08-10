# coding: utf-8
# Author: wanhui0729@gmail.com

import uvicorn
import json
import base64
import numpy as np
import cv2
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ImagesIn(BaseModel):
    images: List[str]


@app.post("/images/{image_id}")
async def image_parse(image_id: int, item: ImagesIn):
    data = json.loads(item.json())
    image_str = data['images'][0]
    image_decode = base64.b64decode(image_str.encode())
    image_np = np.frombuffer(image_decode, np.uint8)
    image = cv2.imdecode(image_np, cv2.COLOR_RGB2BGR)
    cv2.imshow('test.jpg', image)
    cv2.waitKey()

    return {"image_id": image_id}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000, access_log=True, use_colors=True)