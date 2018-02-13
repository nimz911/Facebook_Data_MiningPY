def GetTimestamp(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta

	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
	posts = graph.get_connections(FacebookID,'feed', fields = ['created_time'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break

	post_id = []
	created_time = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j].get('id'))
			created_time.append(posts_data[i][j].get('created_time'))
	
	created_timeDF = pd.DataFrame({'post_id':post_id, 'TimeStamp':created_time})
	created_timeDF = created_timeDF.set_index('post_id')
	created_timeDF['TimeStamp'] =  pd.to_datetime(created_timeDF['TimeStamp'])
	created_timeDF['TimeStamp'] = pd.DatetimeIndex(created_timeDF['TimeStamp']) + timedelta(hours=2) #Add 2 hours to time stamp
	created_timeDF['time'] = created_timeDF['TimeStamp'].dt.time
	created_timeDF['date'] = created_timeDF['TimeStamp'].dt.date
	created_timeDF['WeekDay'] = created_timeDF['TimeStamp'].dt.weekday
	weekdays = ['Monday','Tuesday','Wednesday','Thursday ','Friday','Saturday','Sunday']
	for i in range(len(weekdays)):
		created_timeDF['WeekDay'] = created_timeDF['WeekDay'].replace(i, weekdays[i])
		
	#created_timeDF = created_timeDF.drop('created_time',1)
	end_time = datetime.today()
	
	print '\t'+'CreatedTime_read run time: ' + str(end_time - start_time)[:-7]
	return created_timeDF