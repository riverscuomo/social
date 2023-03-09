def fetch(user):
    """ Fetches the last 800 tweets from the home timeline"""
    print("fetching timeline tweets")
    friends = []
    # https://docs.tweepy.org/en/stable/v1_pagination.html
    # for page in tweepy.Cursor(twitter_v1.home_timeline, tweet_mode="extended",  exclude_replies=True, include_entities=False, count=800).pages(4):
    #     for tweet in page:
    #         json = tweet._json
    #         friends.append(json)
    friends = user.friends(tweet_mode="extended",  count=1000)    
    max_id = friends[-1].id
    print(max_id)
    for i in range(4):
        friends = user.friends(tweet_mode="extended",  count=1000) 
        max_id = friends[-1].id
        print(i, max_id, len(friends))

    
    print(len(friends))
    return friends