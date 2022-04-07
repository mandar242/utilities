#!/usr/bin/env python3
#
# Simplified BSD License https://opensource.org/licenses/BSD-2-Clause)
#

from jira import JIRA
from github import Github
import yaml


with open('config') as f:
    """
    config is a file that contains these keys:
    jira_user: yournamehere
    jira_pw: foobarbaz
    jira_server: https://jira.example.com
    gh_token: ghp_1234567890abcdefghijklmnop
    """
    config = yaml.safe_load(f)


# jiraconn = JIRA(basic_auth=(config['jira_user'], config['jira_pw']), server=config['jira_server'])
jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])

