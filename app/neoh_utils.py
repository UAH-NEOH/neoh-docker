import json
import os
from pathlib import Path


def create_dirs():
    """

    :return:
    """
    # Path("/home/neoh").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/status").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/results").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/request").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/geometry").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/downloads").mkdir(parents=True, exist_ok=True)
    Path("/home/neoh-data/logs").mkdir(parents=True, exist_ok=True)


def update_status(request_id, type, status, message, **kwargs):
    """

    :param request_id:
    :param type:
    :param status:
    :param message:
    :param kwargs:
    :return:
    """
    statusJson = {"request_id": request_id, "type": type, "status": status, "message": message}
    for key, value in kwargs.items():
        statusJson[key] = value

    mydir = '/home/neoh-data/status'
    myfile = request_id + "_status.json"
    folder_path = os.path.join(mydir, myfile)

    with open(folder_path, 'w') as status_file:
        json.dump(statusJson, status_file)
    status_file.close()
