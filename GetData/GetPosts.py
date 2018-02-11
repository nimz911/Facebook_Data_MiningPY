def GetPosts(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta
	start_time = datetime.today()
	posts_data = []
	token = AccessToken
	graph = facebook.GraphAPI(token, version='2.7')
	posts = graph.get_connections(FacebookID,'feed', fields = ['message'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break

	post_id = []
	message = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j].get('id'))
			message.append(posts_data[i][j].get('message'))

	messageDF = pd.DataFrame({'post_id':post_id, 'message':message})
	messageDF = messageDF.set_index('post_id')   
	end_time = datetime.today()
	print '\t'+'Posts_read run time: ' + str(end_time - start_time)[:-7]

	return messageDF