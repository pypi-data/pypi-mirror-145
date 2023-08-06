# https://hackersandslackers.com/python-poetry-package-manager/
import argparse
import sys
import os
import shutil
import json
import requests
import webbrowser
import subprocess
import boto3
from pathlib import Path

def run_local_test():
    # post to the url
    if not os.path.exists(".costack_conf"):
        print("no project information found, initialize first")
        return

    with open(f".costack_conf", "r") as f:
        conf = json.load(f)
    parameters = conf['function_detail']['parameters']
    function_id = conf['function_id']
    # enter the parameters and run the test
    # enter the values for the parameters and use local environment to run the test

    test_image_tag = f"{function_id}:latest"
    print(f"test image tag is {test_image_tag}")

    DOCKER_BUILD_CMD = f"docker build -t {test_image_tag} ."
    DOCKER_RUN_CMD = f"docker run -d -p 9000:8080 {test_image_tag}"
    print(DOCKER_BUILD_CMD)
    subprocess.run(DOCKER_BUILD_CMD, shell=True, check=True)
    print("done building image")
    print("build docker...")
    print(DOCKER_RUN_CMD)
    subprocess.run(DOCKER_RUN_CMD, shell=True, check=True)

    param_json = {}
    for param in parameters:
        # enter the parameters
        param_json[param] = input(f"enter value for {param}: ")
    try:
        subprocess.run(f"curl -XPOST \"http://localhost:9000/2015-03-31/functions/function/invocations\" -d '{json.dumps(param_json)}'", shell=True, check=True)
    except Exception as e:
        # clean the port
        print(f"encountered error {e}")

    print("\n cleaning up local running container")
    STOP_DOCKER_COMMAND = f"docker stop $(docker ps -q --filter ancestor={test_image_tag})"
    subprocess.run(STOP_DOCKER_COMMAND, shell=True, check=True)
