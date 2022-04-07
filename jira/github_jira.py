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

CLOUD_REPOS = ['ansible-collections/amazon.aws',
               'ansible-collections/kubernetes.core',
               'ansible-collections/community.okd',
               'ansible-collections/vmware.vmware_rest']

g = Github(config['gh_token'])
#jiraconn = JIRA(token_auth=config[jira_token']), server=config['jira_server'])
jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])

jira_issues = jiraconn.search_issues('project=ACA and labels=github')

# Component are resource objects
prj_components = jiraconn.project_components(project='ACA')
for comp in prj_components:
    if comp.name == 'Container Native':
        ctn_native_comp = comp
    elif comp.name == 'Public Cloud':
        pub_cloud_comp = comp
    elif comp.name == 'Private Cloud':
        priv_cloud_comp = comp
    else:
        continue

github_issues = []
for repo_name in CLOUD_REPOS:
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(labels=['jira'])
    github_issues.extend(issues)

to_create = []
for bug in github_issues:
    jira_things = [jira_obj.fields.description for jira_obj in jira_issues]
    # If the Github URL does not appear in any github-labelled Jira issue descriptions, we will a new Jira bug
    if not any([bug.html_url in jira_obj.fields.description for jira_obj in jira_issues]):
        to_create.append(bug)

for bug in to_create:
    if bug.repository.name == 'amazon.aws':
        label = 'aws'
        component = pub_cloud_comp
    elif bug.repository.name == 'vmware.vmware_rest':
        label = 'vmware'
        component = priv_cloud_comp
    else:
        label = 'kubernetes'
        component = ctn_native_comp
#    if bug.label = 'CI' or 'ci':

    issue_template = {
        'project': 'ACA',
        'summary': '[{0}/{1}] {2}'.format(bug.repository.name, bug.number, bug.title),
        'description': '{0} \n {1}'.format(bug.html_url, bug.body),
        'issuetype': {'name': 'Bug'},
        'labels': ['github', label],
        'priority': {'name': 'Unprioritized'},
        'components': [{'name': component.name}],
    }
    issue = jiraconn.create_issue(fields=issue_template)
    print(issue.id)
