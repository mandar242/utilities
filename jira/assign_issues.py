#!/usr/bin/env python3

from jira import JIRA
import yaml

with open('config') as f:
    """
    config is a file that contains these keys:
    jira_token: personal access token here
    jira_server: https://jira.example.com
    """
    config = yaml.safe_load(f)

jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])

#aap_issues = jiraconn.search_issues('project=ACA')
#
for issue in ['ACA-267', 'ACA-268', 'ACA-269', 'ACA-270', 'ACA-271']:
    jiraconn.assign_issue(issue, 'mandkulk')

#for i in aap_issues:
#    if i.fields.assignee:
#        print(i.fields.assignee.accountId)
#        #print(issue.raw['fields'])
##print(issue.raw['fields'])
##print(len(aap_issues))
##print(aap_issues[0].fields.assignee.displayName)
#
#for i in aap_issues:
#        if i.fields.assignee:
#            if i.fields.assignee.displayName == 'Display Name':
#                print(i.id, i.key)
