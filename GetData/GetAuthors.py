def GetAuthors(AccessToken, FacebookID): 
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
	posts = graph.get_connections(FacebookID,'feed', fields = ['from'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break
	
	post_id = []
	author_ID = []
	author_name = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j].get('id'))
			if len(posts_data[i][j]) < 2:
				author_ID.append('hidden')
				author_name.append('hidden')
			else:
				author_ID.append(posts_data[i][j].get('from').get('id'))
				author_name.append(posts_data[i][j].get('from').get('name'))
	
	authorsDF = pd.DataFrame({'post_id':post_id, 'author_ID':author_ID, 'author_name':author_name})
	authorsDF = authorsDF.set_index('post_id')

	end_time = datetime.today()
	print '\t'+'Authors_read run time: ' + str(end_time - start_time)[:-3]
	return authorsDF