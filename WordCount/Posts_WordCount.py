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