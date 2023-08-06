import boto3
from costack_cli.utils.requests import get_authorization

def get_boto3_session(team_id):
    access_key, secret_key, _, region = get_authorization(team_id)
    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region)

def create_ecr_repository(ecr_client, function_id):
    response = ecr_client.create_repository(
        repositoryName=function_id,
        imageTagMutability="MUTABLE")
    # print(response)
    code = int(response['ResponseMetadata']['HTTPStatusCode'])
    if (code == 200):
        return {
            "uri": response['repository']['repositoryUri'],
            'arn': response['repository']['repositoryArn']
        }
    else:
        raise Exception("Error creating repo")