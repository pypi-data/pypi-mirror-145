import json
import requests
from costack_cli.constants import BACKEND_ENDPOINT, COSTACK_TOKEN_HEADER_KEY
from costack_cli.config import get_user_login_info


def get_teams():
    user_id, _ = get_user_login_info()
    request_body = {
        "user_id": user_id
    }
    response = requests.post(
        f"{BACKEND_ENDPOINT}/user/teams/get",
        data=json.dumps(request_body),
        headers=_get_headers())
    # print(response)
    response = json.loads(response.text)
    return response["teams"]


def create_function_request(function_id, user_id, team_id, function_name, function_desc, image_uri):
    request_body = {
        "function_id": function_id,
        "user_id": user_id,
        "team_id": team_id,
        "function_name": function_name,
        "function_desc": function_desc,
        "image_uri": image_uri
    }
    response = requests.post(
        f"{BACKEND_ENDPOINT}/functions/create_image_based_function",
        data=json.dumps(request_body),
        headers=_get_headers())
    response = json.loads(response.text)
    return response["function_id"]

def get_authorization(team_id):
    response = requests.get(
        f"{BACKEND_ENDPOINT}/api_route/get_user_authorization_from_team?team_id={team_id}", headers=_get_headers())
    json_load = json.loads(response.text)
    return json_load["access_key"], json_load["secret_key"], json_load["account_id"], json_load["region"]

def update_function_request(team_id, function_id, latest_image_uri):
    request_body = {
        "team_id": team_id,
        "function_id": function_id,
        "image_uri": latest_image_uri
    }
    # print(json.dumps(request_body))
    return requests.post(
        f"{BACKEND_ENDPOINT}/functions/update_function_with_image", 
        data=json.dumps(request_body), 
        headers=_get_headers())

def _get_headers():
    _, token = get_user_login_info()
    return {
        COSTACK_TOKEN_HEADER_KEY: token
    }
