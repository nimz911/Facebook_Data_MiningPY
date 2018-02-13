def FacebookData_read(AccessToken, FacebookID):
    import facebook
    import requests
    import json
    import pandas as pd
    import time
    from datetime import datetime, timedelta
    from multiprocessing.pool import ThreadPool
    from threading import Thread
    

    def FacebookPosts_read(AccessToken, FacebookID):
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
    
    def FacebookCreatedTime_read(AccessToken, FacebookID):
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
        #created_timeDF = created_timeDF.drop('created_time',1)
        end_time = datetime.today()
        
        print '\t'+'CreatedTime_read run time: ' + str(end_time - start_time)[:-7]
        return created_timeDF
    
    def FacebookAuthors_read(AccessToken, FacebookID): 
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

    def FacebookFullPicture_read(AccessToken, FacebookID):
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
    
    def FacebookReactionsCounter(AccessToken, FacebookID):
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

    def FacebookCommentsCounter(AccessToken, FacebookID):
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

    async_result1 = pool1.apply_async(FacebookPosts_read, (AccessToken, FacebookID))
    async_result2 = pool2.apply_async(FacebookCreatedTime_read, (AccessToken, FacebookID))
    async_result3 = pool3.apply_async(FacebookAuthors_read, (AccessToken, FacebookID))
    async_result4 = pool4.apply_async(FacebookFullPicture_read, (AccessToken, FacebookID))
    async_result5 = pool5.apply_async(FacebookReactionsCounter, (AccessToken, FacebookID))
    async_result6 = pool6.apply_async(FacebookCommentsCounter, (AccessToken, FacebookID))
    
    df1 = async_result1.get()
    df2 = async_result2.get()
    df3 = async_result3.get()
    df4 = async_result4.get()
    df5 = async_result5.get()
    df6 = async_result6.get()

    data = df1.join(df2)
    data = data.join(df3)
    data = data.join(df4)
    data = data.join(df5)
    data = data.join(df6)
    
    
    end_time = datetime.today()
    print '\n'+'end time: ' + str(end_time)[:-7]
    print 'total run time: ' + str(end_time - start_time)[:-7]
    
    return data 
