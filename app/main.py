from typing import Union, Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, status
from fastapi.middleware.cors import CORSMiddleware
from urllib.request import Request, urlopen

import string
import json
import random
import os

# NEOH file
from start_cloud_workflow import start_process
from get_result import result_handler

app = FastAPI()

link = "https://filesamples.com/samples/code/json/sample2.json"

req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read().decode('utf-8')

# print(json.loads(webpage))


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {" Welcome to NEOH API"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q, "json": json.loads(webpage)}


class Payload(BaseModel):
    dataset: str
    org_unit: str
    agg_period: str = None
    start_date: str
    end_date: str
    data_element_id: str
    boundaries: List[dict] = []
    stat_type: str = None
    product: str
    var_name: str
    x_start_stride_stop: str = None
    y_start_stride_stop: str = None
    dhis_dist_version: str = None


class Request(BaseModel):
    request_id: str


class Config:
    orm_mode = True


@app.post("/start-process")
def get_payload(payload: Payload):
    # val = ''
    event = payload.dict()
    # event1= json.dumps(event)
    val = start_process(event)

    return val


@app.post("/get-result")
def get_result(request_id: Request):
    # val = ''
    print(request_id)
    event = request_id.dict()
    result = result_handler(event)

    return result
