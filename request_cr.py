import requests, sys, json

import yaml
CONFIG = yaml.load(open("config.yaml"))

gitlab_params = {
	'private_token': CONFIG['GITLAB']['TOKEN'],
	'user': CONFIG['GITLAB']['USER'],
	'state': 'opened'
}
list_mr = json.loads(requests.get(url = CONFIG['GITLAB']['URLS']['LIST_MERGE_REQUESTS'], params = gitlab_params).content)
print(list(map(lambda mr: mr['source_branch'], list_mr)))
mr = list_mr[int('0' + input("Select index of Merge request: "))]


from jira import JIRA
jira_id = CONFIG['JIRA']['TICKET_ID_TEMPLATE'].format(mr['source_branch'][12:16])
jira_ticket = CONFIG['JIRA']['URLS']['LINK_TO_TICKET'].format(jira_id)
gitlab_mr = CONFIG['GITLAB']['URLS']['LINK_TO_MERGE_REQUEST'].format(mr['iid'])

jira = JIRA(basic_auth=(CONFIG['JIRA']['USER'],	CONFIG['JIRA']['TOKEN']), options={'server': CONFIG['JIRA']['URLS']['SERVER']})
jira.add_comment(jira_id, CONFIG['JIRA']['COMMENT'].format(gitlab_mr= gitlab_mr))
jira.transition_issue(jira_id, CONFIG['JIRA']['STATES']['REVIEW_READY'])

slack_params = {
	'token': CONFIG['SLACK']['TOKEN'],
	'channel': CONFIG['SLACK']['CHANNEL'],
	'text': CONFIG['SLACK']['MESSAGE'].format(
		required_cr = 2 - mr['upvotes'],
		jira_ticket = jira_ticket,
		gitlab_mr = gitlab_mr,
	)
}
requests.get(url = CONFIG['SLACK']['URLS']['POST_MESSAGE'], params = slack_params)