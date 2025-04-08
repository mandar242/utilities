#!/usr/bin/env python3
#
# Simplified BSD License https://opensource.org/licenses/BSD-2-Clause)
#

import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager', region_name="us-east-2")
    response = client.get_secret_value(SecretId="cloud_team_jira_login")
    secrets = json.loads(response['SecretString'])

    cloud_team_jira = {
        "jira_user": secrets["cloud_team_jira_user"],
        "jira_pw": secrets["cloud_team_jira_pass"],
        "jira_server": secrets["cloud_team_jira_server"],
        "jira_token": secrets["cloud_team_jira_bot_token"]
    }

    return cloud_team_jira
