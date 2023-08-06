from costack_cli.constants import (
    CONFIG_HOME,
    USER_LOGIN_CONFIG,
    USER_LOGIN_EMAIL_KEY,
    USER_ID_KEY,
    USER_JWT_TOKEN_KEY,
    FUNCTION_CONFIG_PATH,
    FUNCTION_ID_KEY,
    TEAM_ID_KEY,
    ACCOUNT_ID_KEY,
    REGION_KEY
)
import os 
import json
import uuid

def init_config():
    if not os.path.exists(CONFIG_HOME):
        os.mkdir(CONFIG_HOME)

def save_user_credentials(response_json):
    with open(USER_LOGIN_CONFIG, "w") as f:
        json.dump({
            USER_LOGIN_EMAIL_KEY: response_json[USER_LOGIN_EMAIL_KEY],
            USER_ID_KEY: response_json[USER_ID_KEY],
            USER_JWT_TOKEN_KEY: response_json[USER_JWT_TOKEN_KEY]
        }, f)

def get_user_login_info():
    with open(USER_LOGIN_CONFIG, "r") as f:
        login_dict = json.load(f)
        return login_dict[USER_ID_KEY], login_dict[USER_JWT_TOKEN_KEY]
    return None

def save_function_config(function_id, team_id, account_id, region):
    with open(FUNCTION_CONFIG_PATH, "w") as f:
        json.dump({
            FUNCTION_ID_KEY: function_id,
            TEAM_ID_KEY: team_id,
            ACCOUNT_ID_KEY: account_id,
            REGION_KEY: region
        }, f)

def load_function_config():
    with open(FUNCTION_CONFIG_PATH, "r") as f:
        result = json.load(f)
        return result[FUNCTION_ID_KEY], result[TEAM_ID_KEY], result[ACCOUNT_ID_KEY], result[REGION_KEY]
