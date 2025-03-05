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
               'ansible-collections/amazon.cloud',
               'ansible-collections/cloud.terraform',
               'ansible-collections/cloud.common',
               'ansible-collections/community.aws',
               'ansible-collections/community.okd',
               'redhat-cop/cloud.aws_ops',
               'redhat-cop/cloud.aws_troubleshooting',
               'redhat-cop/cloud.gcp_ops',
               'redhat-cop/cloud.terraform_ops',
               'ansible/terraform-provider-aap',
               'ansible/terraform-provider-provider',
]

g = Github(config['gh_token'])
jiraconn = JIRA(token_auth=config['jira_token'], server=config['jira_server'])
jira_issues = jiraconn.search_issues('project=ACA and labels=github', maxResults=1000)

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
jira_things = [jira_obj.fields.description for jira_obj in jira_issues]
for bug in github_issues:
    # jira_things = [jira_obj.fields.description for jira_obj in jira_issues]
    # If the Github URL does not appear in any github-labelled Jira issue descriptions, we will a new Jira bug
    if not any([bug.html_url in jira_obj.fields.description for jira_obj in jira_issues]):
        to_create.append(bug)

dod_title = "Definition of Done"
dod_content = """
* Code Quality: Code adheres to team coding standards and is well-documented.
* Testing: All tests pass successfully, and relevant tests are updated.
* Review and Approval: PR has been reviewed, and feedback has been addressed.
* Documentation: Relevant documentation has been updated (e.g., README, release notes).
* Functionality: Code meets requirements and works as expected without regressions.
* Merging: PR is up to date with the base branch and free of merge conflicts.
* Backporting: Relevant backport labels are added based on the nature of the fix, and backported PRs are approved and merged.
"""

for bug in to_create:
    if bug.repository.name in ['amazon.aws', 'community.aws']:
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
        'description': '{0} \n {1} \n h3. {2} \n {3}'.format(bug.html_url, bug.body, dod_title, dod_content),
        'issuetype': {'name': 'Bug'},
        'labels': ['github', label],
        'priority': {'name': 'Undefined'},
        'components': [{'name': component.name}, {'name': 'cloud-content'}],
        'versions':  [{'id': '12398634'}],
    }
#versions = jiraconn.project_versions('ACA')
#print([v for v in reversed(versions)])
#[<JIRA Version: name='2.5', id='12401238'>, <JIRA Version: name='Unspecified', id='12398634'>, <JIRA Version: name='2.4', id='12397364'>, <JIRA Version: name='2.3', id='12385838'>]
    issue = jiraconn.create_issue(fields=issue_template)
    print(issue.id)
    # Transition the issue from New to Backlog
    jiraconn.transition_issue(issue.id, "Backlog")

