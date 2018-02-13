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


    df1 = pd.DataFrame({'author_id':author_id, 'join_date':join_date})
    df1 = df1.set_index('author_id')

    author_id = []
    author_name = []
    for i in range(len(members_name_data)):
        for j in range(len(members_name_data[i])):
            author_id.append(members_name_data[i][j].get('id'))
            author_name.append(members_name_data[i][j].get('name'))

    df2 = pd.DataFrame({'author_id':author_id, 'member':author_name})
    df2 = df2.set_index('author_id')


    membersDF = df1.join(df2)
    membersDF['join_date'] = pd.to_datetime(membersDF['join_date'],unit='s')
    membersDF['TimeDelta'] = pd.datetime.now().date() - pd.to_datetime(membersDF['join_date'],unit='s')
    membersDF['Days_in_Group'] = membersDF['TimeDelta'].dt.total_seconds()/(24 * 60 * 60)
    membersDF['Days_in_Group'] = membersDF['Days_in_Group'].round()
    membersDF = membersDF.drop('TimeDelta',1)
    membersDF = membersDF.sort_values('Days_in_Group', axis=0, ascending=False)
    end_time = datetime.today()
    print '\t'+'GetMembers run time: ' + str(end_time - start_time)[:-7]
    return membersDF