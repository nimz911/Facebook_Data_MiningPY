def GetCommentsCounter(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta

	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
	posts = graph.get_connections(FacebookID,'feed', fields = ['comments.limit(0).summary(true)'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break

	post_id = []
	comments_count = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j]['id'])
			comments_count.append(posts_data[i][j]['comments']['summary']['total_count'])

	CommentsCount = pd.DataFrame({'post_id':post_id, 'comments_count':comments_count})
	CommentsCount = CommentsCount.set_index('post_id')
	
	end_time = datetime.today()
	print '\t'+'CommentsCount run time: ' + str(end_time - start_time)[:-7]
	return CommentsCount