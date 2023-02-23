from typing import Union, Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from urllib.request import Request, urlopen

import string
import json
import random
import os

# NEOH file
from start_cloud_workflow import start_process
from get_result import result_handler
from download_imerg import lambda_handler
from download_aggregate_opendap_modis import modis_handler
from download_aggregate_opendap_imerg import imerg_handler


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
async def get_payload(payload: Payload, background_tasks: BackgroundTasks):
    # val = ''
    event = payload.dict()
    # event1= json.dumps(event)
    payload_process = start_process(event)
    print(payload_process)
    print('out of process func')
    if payload_process['dataset'].lower() == 'precipitation':
        print("Calling the handler for: " + payload_process['dataset'])
        # background_tasks.add_task(lambda_handler, payload_process['json'])
        imerg_handler(payload_process['json'])
        # lambda_handler(payload_process['json'])

    elif payload_process['dataset'].lower() == 'temperature' or 'vegetation':
        print("Calling the handler for: " + payload_process['dataset'])
        # background_tasks.add_task(modis_handler, payload_process['json'])
        print(payload_process['json']['request_id'])
        # pay = {"dataset": "temperature", "org_unit": "district", "agg_period": "daily", "start_date": "2020-01-01T00:00:00.000Z", "end_date": "2020-01-21T00:00:00.000Z", "data_element_id": "8675309", "request_id": payload_process['json']['request_id'], "min_lat": 6.9176, "max_lat": 10.0004, "min_lon": -13.3035, "max_lon": -10.2658, "creation_time": "02-21-2023T18:58:49Z", "stat_type": "mean", "product": "MOD11B2", "var_name": "LST_Day_6km", "dhis_dist_version": "sierra_leone_1"}
        modis_handler(payload_process['json'])

    return payload_process


@app.post("/get-result")
def get_result(request_id: Request):
    # val = ''
    print(request_id)
    event = request_id.dict()
    result = result_handler(event)

    return result
