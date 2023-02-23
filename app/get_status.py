# import json
# import boto3
# from botocore.exceptions import ClientError
#
# data_bucket = "mosquito-data"
#
# s3 = boto3.client('s3')
#
#
# def lambda_handler(event, context):
#     print("event ", event)
#
#     if 'body' in event:
#         try:
#             event = json.loads(event['body'])
#         except (TypeError, ValueError):
#             return dict(statusCode='200',
#                         headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
#                                  'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
#                                  'Access-Control-Allow-Methods': 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},
#                         body=json.dumps({'message': "missing json parameters"}), isBase64Encoded='false')
#
#     request_id = event['request_id']
#
#     all_result = []
#
#     for request_id_obj in request_id:
#
#         key_file = "status/" + request_id_obj + ".json"
#
#         try:
#             data = s3.get_object(Bucket=data_bucket, Key=key_file)
#             status = {"message": "error"}
#             status = json.loads(data['Body'].read().decode('utf-8'))
#             print(data)
#         except ClientError as ex:
#             print(ex)
#             status = {"message": "error"}
#
#         # status = load_json_from_s3(my_bucket, )
#         print(status)
#         if "message" in status and status['message'] == "error":
#             result_json = {"status": "waiting", "message": "Job not started yet for request_id " + request_id_obj,
#                            "request_id": request_id_obj, "type": "waiting", "creation_time": "n/a"}
#         else:
#             result_json = status
#         all_result.append(result_json)
#
#     return dict(statusCode='200', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
#                                            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
#                                            'Access-Control-Allow-Methods': 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'},
#                 body=json.dumps(all_result), isBase64Encoded='false')