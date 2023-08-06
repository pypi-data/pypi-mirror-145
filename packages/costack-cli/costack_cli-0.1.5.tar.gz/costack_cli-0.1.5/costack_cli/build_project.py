import os
import uuid
import subprocess
import base64
from costack_cli.utils.aws_helpers import create_ecr_repository, get_boto3_session
from costack_cli.utils.requests import update_function_request
from costack_cli.config import load_function_config
from costack_cli.constants import BACKEND_ENDPOINT
from costack_cli.config import init_config, get_user_login_info, save_function_config
from costack_cli.utils.requests import get_teams, create_function_request, get_authorization

def get_image_uri(account_id, region, repository_name):
    return f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}"


def tag_latest_uri(image_uri):
    return f"{image_uri}:latest"


def get_registry_access_token(ecr_client, repo_id):
    response = ecr_client.get_authorization_token(
        registryIds=[
            repo_id,
        ]
    )

    return base64.b64decode(response['authorizationData'][0]['authorizationToken']).decode('utf-8')[4:]

def build_and_push_image(ecr_access_token, function_id, latest_image_uri, account_id, region):
    # invoke docker to build image
    subprocess.run(
        [f"docker login --username AWS --password {ecr_access_token} {account_id}.dkr.ecr.{region}.amazonaws.com"], shell=True)
    subprocess.run([f"docker build -t {function_id} ."], shell=True)
    subprocess.run(
        [f"docker tag {function_id}:latest {latest_image_uri}"], shell=True)
    subprocess.run([f"docker push {latest_image_uri}"], shell=True)

def update_function():
    function_id, team_id, _, _ = load_function_config()
    image_uri = _build_image()
    update_function_request(team_id, function_id, image_uri)
    print("Model successfully updated!")

def create_function(team_id, function_name, function_desc):
    user_id, _ = get_user_login_info()
    _, _, account_id, region = get_authorization(team_id)
    function_id = str(uuid.uuid4())
    save_function_config(function_id, team_id, account_id, region)
    boto3_session = get_boto3_session(team_id)
    ecr_client = boto3_session.client('ecr')
    create_ecr_repository(ecr_client, function_id)
    image_uri = _build_image()
    create_function_request(
        function_id,
        user_id,
        team_id, 
        function_name,
        function_desc, 
        image_uri)

def _build_image():
    # validate_project_folder()
    function_id, team_id, account_id, region = load_function_config()
    boto3_session = get_boto3_session(team_id)
    ecr_client = boto3_session.client('ecr')

    latest_image_uri = tag_latest_uri(get_image_uri(account_id, region, function_id))
    access_token = get_registry_access_token(ecr_client, account_id)
    build_and_push_image(access_token, function_id,
                         latest_image_uri, account_id, region)
    return latest_image_uri


