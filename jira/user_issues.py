#!/usr/bin/env python3

from jira import JIRA
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

jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])

aap_issues = jiraconn.search_issues('project=ACA')

#print(issue.raw['fields'])
#print(len(aap_issues))
#print(aap_issues[0].fields.assignee.displayName)

for i in aap_issues:
        if i.fields.assignee:
            if i.fields.assignee.displayName == 'Person Person':
                print(i.id, i.key)
