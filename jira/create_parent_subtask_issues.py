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
    jira_token: personal access token
    jira_user: yournamehere
    jira_pw: foobarbaz
    jira_server: https://jira.example.com
    gh_token: ghp_1234567890abcdefghijklmnop
    """
    config = yaml.safe_load(f)

jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])
module_list = ['iam_user', 'iam_policy', 'lambda', 'route53']


# Component are resource objects
prj_components = jiraconn.project_components(project='ACA')
for comp in prj_components:
    if comp.name == 'Public Cloud':
        pub_cloud_comp = comp
    else:
        continue


label = 'aws'
component = pub_cloud_comp

module_description = '''
Ensure that code is free of known bugs
Ensure that module meets the coding and functionality criteria for support:

* blahblahblah 
'''
ci_description = '''
Ensure that the module and accompanying _info module have stable, supported, enabled integration tests and CI is green.  Tests should adhere to the criteria in https://docs.ansible.com/ansible/devel/dev_guide/platforms/aws_guidelines.html#integration-tests-for-aws-modules

https://github.com/ansible/community/blob/main/group-aws/integration.md 
* blahblahblah

NOTE: If the module can not reasonably be integration tested it must have unit tests.
'''

for module_name in module_list:
    # customfield_12311140 is Epics in RH's Jira instance
    issue_template = {
        'project': 'ACA',
        'summary': 'Stabilize and prepare {0} and {0}_info modules and tests to be migrated to amazon.aws'.format(module_name),
        'description': 'Stabilize {0}* modules'.format(module_name),
        'issuetype': {'name': 'Story'},
        'labels': [label],
        'priority': {'name': 'Major'},
        'components': [{'name': component.name}],
        'customfield_12311140': 'ACA-412'
    }
    issue = jiraconn.create_issue(fields=issue_template)
    print(issue.id)

    module_subtasktemplate = {
        'project': 'ACA',
        'summary': 'Stabilize {0} module'.format(module_name),
        'description': module_description,
        'issuetype': {'name': 'Sub-task'},
        'labels': [label],
        'priority': {'name': 'Major'},
        'components': [{'name': component.name}],
        'parent' : { 'id' : issue.id}
    }
    
    info_subtasktemplate = {
        'project': 'ACA',
        'summary': 'Stabilize {0}_info module'.format(module_name),
        'description': ci_description,
        'issuetype': {'name': 'Sub-task'},
        'labels': [label],
        'priority': {'name': 'Major'},
        'components': [{'name': component.name}],
        'parent' : { 'id' : issue.id}
    }
    
    ci_subtasktemplate = {
        'project': 'ACA',
        'summary': 'CI enablement for {0}* modules'.format(module_name),
        'description': module_description,
        'issuetype': {'name': 'Sub-task'},
        'labels': [label],
        'priority': {'name': 'Major'},
        'components': [{'name': component.name}],
        'parent' : { 'id' : issue.id}
    }
    for subtask in module_subtasktemplate, info_subtasktemplate, ci_subtasktemplate:
        child = jiraconn.create_issue(fields=subtask)
        print(child.key)

