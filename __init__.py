def GetMembers(AccessToken, FacebookID):
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    import facebook
    import requests
    import json
    import pandas as pd
    import time
    from datetime import datetime, timedelta
    
    start_time = datetime.today()
    members_data = []
    members_name_data = []
    graph = facebook.GraphAPI(AccessToken, version='2.7')
    members = graph.get_connections(FacebookID,'members', fields = ['joined'])
    members_name = graph.get_connections(FacebookID,'members')
    members_data.append(members['data'])
    members_name_data.append(members_name['data'])


    while(1):
        if 'paging' in members and 'next' in members['paging']:
            members = requests.get(members['paging']['next']).json()
            members_data.append(members['data'])

        else:
            break

    while(1):
        if 'paging' in members_name and 'next' in members_name['paging']:
            members_name = requests.get(members_name['paging']['next']).json()
            members_name_data.append(members_name['data'])

        else:
            break

    author_id = []
    join_date = []
    for i in range(len(members_data)):
        for j in range(len(members_data[i])):
            author_id.append(members_data[i][j].get('id'))
            join_date.append(members_data[i][j].get('joined'))


    df1 = pd.DataFrame({'author_ID':author_id, 'join_date':join_date})
    df1 = df1.set_index('author_ID')

    author_id = []
    author_name = []
    for i in range(len(members_name_data)):
        for j in range(len(members_name_data[i])):
            author_id.append(members_name_data[i][j].get('id'))
            author_name.append(members_name_data[i][j].get('name'))

    
	
	df2 = pd.DataFrame({'author_ID':author_id, 'member':author_name})
	df2 = df2.set_index('author_ID')
	membersDF = df1.join(df2)
	membersDF['join_date'] = pd.to_datetime(membersDF['join_date'],unit='s')
	membersDF['TimeDelta'] = pd.datetime.now().date() - pd.to_datetime(membersDF['join_date'],unit='s')
	membersDF['Days_in_Group'] = membersDF['TimeDelta'].dt.total_seconds()/(24 * 60 * 60)
	membersDF['Days_in_Group'] = membersDF['Days_in_Group'].round()
	membersDF = membersDF.drop('TimeDelta',1)
	membersDF = membersDF.sort_values('Days_in_Group', axis=0, ascending=False)
	membersDF = membersDF.reset_index()
	membersDF = membersDF.drop(['member'],1)
	
    end_time = datetime.today()
	
    print '\t'+'GetMembers run time: ' + str(end_time - start_time)[:-7]
    return membersDF

def GetPosts(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta
	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
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
		
def GetAuthors(AccessToken, FacebookID): 
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta

	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
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
	
def GetFullPictureLink(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta

	start_time = datetime.today()
	posts_data = []
	graph = facebook.GraphAPI(AccessToken, version='2.7')
	posts = graph.get_connections(FacebookID,'feed', fields = ['full_picture'])
	posts_data.append(posts['data'])

	while(1):
		if 'paging' in posts and 'next' in posts['paging']:
			posts = requests.get(posts['paging']['next']).json()
			posts_data.append(posts['data'])

		else:
			break

	post_id = []
	full_picture = []
	for i in range(len(posts_data)):
		for j in range(len(posts_data[i])):
			post_id.append(posts_data[i][j].get('id'))
			full_picture.append(posts_data[i][j].get('full_picture'))
	
	full_pictureDF = pd.DataFrame({'post_id':post_id, 'full_picture':full_picture})
	full_pictureDF = full_pictureDF.set_index('post_id')

	end_time = datetime.today()
	print '\t'+'full_picture run time: ' + str(end_time - start_time)[:-7]
	return full_pictureDF
    
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
	
def FacebookData_read(AccessToken, FacebookID):
	import facebook
	import requests
	import json
	import pandas as pd
	import time
	from datetime import datetime, timedelta
	from multiprocessing.pool import ThreadPool
	from threading import Thread
	
	graph = facebook.GraphAPI(AccessToken, version='2.7')
	name = graph.get_object(FacebookID).get('name')
	print '##### getting data from: ' + name + ' #####'+'\n'

	start_time = datetime.today()
	print 'start time: ' + str(start_time)[:-7] + '\n'

	pool1 = ThreadPool(processes=1)
	pool2 = ThreadPool(processes=1)
	pool3 = ThreadPool(processes=1)
	pool4 = ThreadPool(processes=1)
	pool5 = ThreadPool(processes=1)
	pool6 = ThreadPool(processes=1)
	pool7 = ThreadPool(processes=1)

	async_result1 = pool1.apply_async(GetPosts, (AccessToken, FacebookID))
	async_result2 = pool2.apply_async(GetTimestamp, (AccessToken, FacebookID))
	async_result3 = pool3.apply_async(GetAuthors, (AccessToken, FacebookID))
	async_result4 = pool4.apply_async(GetFullPictureLink, (AccessToken, FacebookID))
	async_result5 = pool5.apply_async(GetReactionsCounter, (AccessToken, FacebookID))
	async_result6 = pool6.apply_async(GetCommentsCounter, (AccessToken, FacebookID))
	async_result7 = pool7.apply_async(GetMembers, (AccessToken, FacebookID))

	PostsDF = async_result1.get()
	TimestampDF = async_result2.get()
	AuthorDF = async_result3.get()
	FullPictureLinkDF = async_result4.get()
	ReactionsCounterDF = async_result5.get()
	CommentsCounterDF = async_result6.get()
	members = async_result7.get()

	data = PostsDF.join(TimestampDF)
	data = data.join(AuthorDF)
	data = data.join(FullPictureLinkDF)
	data = data.join(ReactionsCounterDF)
	data = data.join(CommentsCounterDF)
	
	membersDF_sum = data.groupby(['author_ID','author_name']).sum().sort_values('comments_count', ascending=False)
	membersDF_count = data.groupby(['author_ID','author_name']).count().sort_values('comments_count', ascending=False)['TimeStamp']
	membersDF = membersDF_sum.join(membersDF_count).rename(columns={'TimeStamp': 'Post_Count'})
	
	membersDF['reactions_AVG'] = membersDF['reactions_count'] / membersDF['Post_Count']
	membersDF['comments_AVG'] = membersDF['comments_count'] / membersDF['Post_Count']
	membersDF = membersDF.sort_values('comments_AVG', ascending=False)
	membersDF = membersDF.reset_index() 
	
	membersDF = membersDF.join(members, lsuffix='_L', rsuffix="_R")
	membersDF = membersDF.drop(['author_ID_R'],1)
	membersDF = membersDF.rename(columns={'author_ID_L': 'memberID'})

	end_time = datetime.today()
	print '\n'+'end time: ' + str(end_time)[:-7]
	print 'total run time: ' + str(end_time - start_time)[:-7]

	return data, membersDF

def Posts_WordCount(AccessToken, FacebookID):
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    import facebook
    import requests
    import json
    import pandas as pd
    import time
    from datetime import datetime, timedelta
    
    start_time = datetime.today()
    posts_data = []
    graph = facebook.GraphAPI(AccessToken, version='2.7')
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
    
    text = messageDF['message'].to_string()
    tokens = word_tokenize(text)

    stops = set(stopwords.words('english'))
    pun = ['\'','.',',','(',')','[',']','...','&','!']
    txt = []
    for word in tokens:
        word = word.lower()
        if word not in stops:
            if word not in pun:
                if len(word) > 2 and len(word) <= 25 and word != 'none':
                    txt.append(word)

    WordCount = pd.DataFrame(txt)
    WordCount = pd.DataFrame(WordCount[0].value_counts())

    end_time = datetime.today()
    print '\t'+'Posts_read run time: ' + str(end_time - start_time)[:-7]

    return WordCount