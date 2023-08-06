# https://hackersandslackers.com/python-poetry-package-manager/
import argparse
import os
from costack_cli.sample_files import COSTACK_MAIN, DOCKER_CONTENT, REQUIREMENTS_CONTENT, TRAIN_CONTENT, DOCKET_IGNORE_CONTENT
from costack_cli.build_project import create_function, update_function
from costack_cli.local_test import run_local_test
from costack_cli.login import do_login_with_web_portal
from costack_cli.config import init_config, get_user_login_info, save_function_config
from costack_cli.utils.requests import get_teams, create_function_request, get_authorization
from costack_cli.utils.aws_helpers import create_ecr_repository, get_boto3_session
import inquirer

def init_dev_environment():
    
    team_list = get_teams()
    # print(team_list)
    team_name_list = [x["name"] for x in team_list]
    questions = [
        inquirer.Text("function_name", "Name of the model created"),
        inquirer.Text("function_desc", "Description of the model created"),
        inquirer.Text("handler", message="Handler location that processes the request (<file name>.<method name>)", default="costack_main.handler"),
        inquirer.List('team_name',
            message="Which team do you want your model be in: ",
            choices=team_name_list
        )
    ]

    question_result = inquirer.prompt(questions)
    team_id = ""
    for team_record in team_list:
        if team_record["name"] == question_result["team_name"]:
            team_id = team_record["id"]
    # also initialize the required files
    # make requirement file
    with open("requirements.txt", "w") as f:
        f.write(REQUIREMENTS_CONTENT)
        f.close()
    # write the function file
    with open(f"costack_main.py", "w") as f:
        f.write(COSTACK_MAIN)
        f.close()
    with open(f"Dockerfile", "w") as f:
        f.write(DOCKER_CONTENT)
        f.close()
    
    with open(f"train.py", "w") as f:
        f.write(TRAIN_CONTENT)
        f.close()
    with open(f".dockerignore", "w") as f:
        f.write(DOCKET_IGNORE_CONTENT)
        f.close()
    if not os.path.exists("model"):
        os.mkdir("model")

    if not os.path.exists("data"):
        os.mkdir("data")
    create_function(
        team_id, 
        question_result["function_name"], 
        question_result["function_desc"])
    
    print("Function initialization completed. You can go to the console to view your function!")

def main(command_line=None):
    # base parser
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    login = subparser.add_parser('login')
    login.add_argument('-u', '--username', type=str, required=False)
    login.add_argument('-p', '--password', type=str, required=False)

    init = subparser.add_parser('init')

    local_test = subparser.add_parser('test')
    local_test.add_argument('--debug', type=str, default=False, required=False)

    deploy = subparser.add_parser('deploy')
    deploy.add_argument('--debug', type=str, default=False, required=False)
    deploy.add_argument('--update', action='store_true')

    args = parser.parse_args()

    init_config()

    if args.command == 'login':
        do_login_with_web_portal()

    elif args.command == 'init':
        init_dev_environment()
    elif args.command == 'test':
        run_local_test()
    elif args.command == 'deploy':
        update_function()

if __name__ == '__main__':
    main()
