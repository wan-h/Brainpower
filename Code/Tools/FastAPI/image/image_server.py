# coding: utf-8
# Author: wanhui0729@gmail.com

import uvicorn
import json
import base64
import numpy as np
import os, sys
import cv2
from io import BytesIO
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from PIL import Image

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

app = FastAPI()

class ImagesIn(BaseModel):
    images: List[str]

class ImagesBytesIn(BaseModel):
    images: str

class ImagesNumpyIn(BaseModel):
    shape: List
    data: str

@app.post("/images/base64/{image_id}")
async def image_base64_parse(image_id: int, item: ImagesIn):
    data = json.loads(item.json())
    image_str = data['images'][0]
    image_decode = base64.b64decode(image_str.encode())
    image_np = np.frombuffer(image_decode, np.uint8)
    image = cv2.imdecode(image_np, cv2.COLOR_RGB2BGR)
    # cv2.imshow('test.jpg', image)
    # cv2.waitKey()
    return {"image_id": image_id}

async def image_file_parse(image_id: int, file: UploadFile = File(...)):
    image_tmp_file = file.file
    image_bytes_stream = BytesIO(image_tmp_file.read())
    capture_image = Image.open(image_bytes_stream)
    image = cv2.cvtColor(np.asarray(capture_image), cv2.COLOR_RGB2BGR)
    # cv2.imshow('test.jpg', image)
    # cv2.waitKey()
    return {"image_id": image_id}

@app.post("/images/numpy/{image_id}")
async def image_numpy_parse(image_id: int, shape: str, file: UploadFile = File(...)):
    image_tmp_file = file.file
    image_np = np.frombuffer(image_tmp_file.read(), np.uint8)
    shape = json.loads(shape)
    image_np = image_np.reshape(shape)
    # cv2.imshow('test.jpg', image_np)
    # cv2.waitKey()
    return {"image_id": image_id}
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000, access_log=True, use_colors=True)