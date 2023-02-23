#! /usr/bin/python3
import argparse
from subprocess import run
from os import system
import os


def create_lambda_function(create_func_name, program_name, run_time, zip_file, handler_name, role):
    """

    :return:
    """
    program_name
    zip_file_name = f"fileb://{zip_file}"
    create_lambda_cmd = run(
        ['awslocal', 'lambda', 'create-function', '--function-name', create_func_name, '--runtime',
         run_time, '--zip-file', zip_file_name, '--handler', handler_name, '--role', role], shell=True, check=False)

    # system("awslocal lambda create-function --function-name my-function --runtime python3.9
    # --zip-file fileb:///Users/nselvaraj/localstack/lambdas/program.zip
    # --handler program.lambda_handler --role arn:aws:iam::000000000000:role/lambda-ex")

    print(create_lambda_cmd.stdout)


def update_lambda_function(update_func_name, zip_file):
    """

    :return:
    """
    update_lambda_cmd = run(
        ['awslocal', 'lambda', 'update-function-code', '--function-name', update_func_name, '--zip-file',
         zip_file], shell=True, check=False,
        capture_output=True)
    print(update_lambda_cmd.stdout)


def invoke_lambda_function(invoke_func_name, payload, out_file):
    """

    :return:
    """
    invoke_lambda_cmd = run(
        ['awslocal', 'lambda', 'invoke', '--function-name', invoke_func_name, '--invocation-type',
         'RequestResponse', '--payload', payload, out_file, '--log-type', 'Tail'], shell=True, check=False,
        capture_output=True)
    print(invoke_lambda_cmd.stdout)


def delete_lambda_function(delete_func_name):
    """

    :return:
    """
    delete_lambda_cmd = run(
        ['awslocal', 'lambda', 'delete-function', '--function-name', delete_func_name], shell=True, check=False,
        capture_output=True)
    print(delete_lambda_cmd.stdout)


def create_roles():
    """
    Creating Roles for Lambda function
    :return:
    """
    try:
        system(
            """awslocal iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": 
            "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, 
            "Action": "sts:AssumeRole"}]}'""")
        system(
            "awslocal iam attach-role-policy --role-name lambda-ex --policy-arn "
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
    except Exception as e:
        print(str(e))


def start_docker_compose():
    """
    Execute the Docker compose up command
    :return:
    """
    try:
        docker_compose_cmd = run(['docker-compose', 'up'], capture_output=True)
        print(docker_compose_cmd.stdout)
    except Exception as e:
        print(str(e))


def stop_docker_compose():
    """
    Execute the Docker compose down command
    :return:
    """
    try:
        docker_compose_cmd = run(['docker-compose', 'down'], capture_output=True)
        print(docker_compose_cmd.stdout)
    except Exception as e:
        print(str(e))


def main():
    parser = argparse.ArgumentParser(description='To run localstack and AWSlocal.')
    parser.add_argument('-c', '--create', dest='create_func_name', nargs='?',
                        help='Create a lambda function in local aws')
    parser.add_argument('-i', '--invoke', dest='invoke_func_name', nargs='?',
                        help='Invoke the lambda function in local aws')
    parser.add_argument('-u', '--update', dest='update_func_name', nargs='?',
                        help='Update the lambda function in local aws')
    parser.add_argument('-d', '--delete', dest='delete_func_name', nargs='?',
                        help='Delete the lambda function in local aws')
    parser.add_argument('-p', '--program', dest='program_name', nargs='?', required=True,
                        help='Program name of the Lambda function')
    parser.add_argument('-ru', '--runtime', dest='run_time', nargs='?', default="python3.9",
                        help='Run time of the lambda function in local aws')
    parser.add_argument('-z', '--zip', dest='program_file', nargs='?', default="./lambdas/program.zip",
                        help='Program file location of lambda function in local aws')
    parser.add_argument('-ha', '--handler', dest='handler_name', nargs='?', default="program.lambda_handler",
                        help='handler of the lambda function in local aws')
    parser.add_argument('-ro', '--role', dest='role', nargs='?', default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Role ARN of the lambda function in local aws')
    parser.add_argument('-s', '--stop', dest='stop_docker', nargs='?',
                        help='Stop Docker ')
    parser.add_argument('-pay', '--payload', dest='payload', nargs='?',
                        default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Input for the lambda function in local aws')
    parser.add_argument('-o', '--output', dest='out_file', nargs='?',
                        help='To store the output from Lambda ')
    args = parser.parse_args()

    create_func_name, invoke_func_name, update_func_name, delete_func_name, \
    program_name, run_time, program_file, \
    handler_name, role, stop_docker, payload, out_file = [vars(args).get(ele) for ele in args.__dict__.keys()]

    start_docker_compose()
    create_roles()
    if create_func_name is not None:
        print("Creaing the Lambda function: {}".format(create_func_name))
        create_lambda_function(create_func_name, program_name, run_time, program_file, handler_name, role)
    if invoke_func_name is not None:
        print("Invoking the Lambda function: {}".format(invoke_func_name))
        invoke_lambda_function(invoke_func_name, payload, out_file)
    if update_func_name is not None:
        print("Updating the Lambda function: {}".format(update_func_name))
        update_lambda_function(update_func_name, program_file)
    if delete_func_name is not None:
        delete_lambda_function(delete_func_name)
    if stop_docker is not None:
        stop_docker_compose()
    #
    # print("end")


if __name__ == "__main__":
    main()
