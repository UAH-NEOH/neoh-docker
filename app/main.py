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
from get_status import status_handler
from start_cloud_workflow import start_process
from get_result import result_handler
from download_aggregate_opendap_modis import modis_handler
from download_aggregate_opendap_imerg import imerg_handler

app = FastAPI()

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

class Status(BaseModel):
    request_id: list

class Config:
    orm_mode = True


@app.post("/start-process")
async def get_payload(payload: Payload, background_tasks: BackgroundTasks):
    event = payload.dict()
    payload_process = start_process(event)
    print(payload_process)

    if payload_process['dataset'].lower() == 'precipitation':
        print("Calling the handler for: " + payload_process['dataset'])
        background_tasks.add_task(imerg_handler, payload_process['json'])
        # imerg_handler(payload_process['json'])

    elif payload_process['dataset'].lower() == 'temperature' or 'vegetation':
        print("Calling the handler for: " + payload_process['dataset'])
        background_tasks.add_task(modis_handler, payload_process['json'])
        # modis_handler(payload_process['json'])

    return payload_process


@app.post("/get-result")
def get_result(request_id: Request):
    print(request_id)
    event = request_id.dict()
    result = result_handler(event)

    return result


@app.post("/get-status")
def get_status(request_id: Status):
    print(request_id)
    event = request_id.dict()
    result = status_handler(event)

    return result
