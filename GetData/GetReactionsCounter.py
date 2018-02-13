def GetReactionsCounter(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta

	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
	posts = graph.get_connections(FacebookID,'feed', fields = ['reactions.limit(0).summary(true)'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break

	post_id = []
	reactions_count = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j]['id'])
			reactions_count.append(posts_data[i][j]['reactions']['summary']['total_count'])

	ReactionsCount = pd.DataFrame({'post_id':post_id, 'reactions_count':reactions_count})
	ReactionsCount = ReactionsCount.set_index('post_id')
	end_time = datetime.today()
	print '\t'+'ReactionsCount run time: ' + str(end_time - start_time)[:-7]
	
	return ReactionsCount