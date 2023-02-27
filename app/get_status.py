import json
import os


def status_handler(event):
    print(event)
    request_id = event['request_id']
    all_result = []
    #
    for request_id_obj in request_id:
        mydir = '/home/neoh-data/status'
        myfile = request_id_obj + "_status.json"
        folder_path = os.path.join(mydir, myfile)
        try:
            with open(folder_path, 'r') as json_file:
                resultJson = json.load(json_file)
            json_file.close()

        except:
            print('File is not ready yet')

            resultJson = {"request_id": request_id_obj,
                          "type": "waiting",
                          "status": "Info",
                          "message": "File not available/Job not started", "creation_time": "n/a"
                          }
        all_result.append(resultJson)
    return all_result


