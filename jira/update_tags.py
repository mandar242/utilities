from jira import JIRA

with open('credentials') as f:
    jira_pw = f.read()

jiraconn = JIRA(token_auth=config['jira_token'], server='https://issues.redhat.com/')

aws_issues = jiraconn.search_issues('project=ACA and labels=aws')

for i in aws_issues:
    if 'inventory' not in i.fields.summary:
        i.update(fields={'labels': ['2.0.0', 'aws']})
