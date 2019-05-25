import os

import yaml
CONFIG = yaml.load(open("config.yaml"))

os.chdir(CONFIG['SETTINGS']['PROJECT_FOLDER'])
 
from jira import JIRA
jira = JIRA(basic_auth=(CONFIG['JIRA']['USER'],	CONFIG['JIRA']['TOKEN']), options={'server': CONFIG['JIRA']['URLS']['SERVER']})
issues = jira.search_issues('project={project_name} and assignee = currentUser() and status="{status}" and sprint in openSprints () order by priority'.format(
	project_name = CONFIG['JIRA']['PROJECT_NAME'],
	status = CONFIG['JIRA']['STATES']['TO_DO'],
))
print(list(map(lambda i: i.fields.summary, issues)))
issue = issues[int('0' + input("Select index of Issue: "))]

branch_name = "{ticket_id}/{ticket_summary}".format(
	ticket_id = issue.key,
	ticket_summary = issue.fields.summary.strip()
	.replace(' - ', '-')
	.replace(' ', '-')
	.replace("'", '')
	.replace('"', '')
	.lower())
print(branch_name)
os.system('git checkout develop && git pull && git flow feature start {}'.format(branch_name))
jira.transition_issue(jira_id, CONFIG['JIRA']['STATES']['IN_PROGRESS'])
