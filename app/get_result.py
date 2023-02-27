import json
import os


def result_handler(event):
    print(event)
    request_id = event['request_id']

    mydir = '/home/neoh-data/results'
    myfile = request_id + "_result.json"
    folder_path = os.path.join(mydir, myfile)
    try:
        with open(folder_path, 'r') as json_file:
            resultJson = json.load(json_file)
        json_file.close()
    except:
        print('File is not ready yet')
        resultJson = {"request_id": request_id,
                      "type": "waiting",
                      "status": "Info",
                      "message": "File not available/Job not started", "creation_time": "n/a"
                      }
    return resultJson
