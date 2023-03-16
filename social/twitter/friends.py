import tweepy 

def fetch(twitter_v1, screen_name):
    """ Fetches friends for a user """
    print("fetching friends")
    friends = []
    # https://docs.tweepy.org/en/stable/v1_pagination.html
    # for page in tweepy.Cursor(twitter_v1.home_timeline, tweet_mode="extended",  exclude_replies=True, include_entities=False, count=800).pages(4):
    #     for tweet in page:
    #         json = tweet._json
    #         friends.append(json)
    # friends = user.friends(tweet_mode="extended",  count=200)    
    # max_id = friends[-1].id
    # print(max_id)
    # for i in range(4):
    #     next_batch = user.friends(tweet_mode="extended",  count=200, max_id=max_id ) 
    #     max_id = next_batch[-1].id
    #     friends += next_batch
    #     print(i, max_id, len(friends))

    
    # https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    friends = []
    for friend in tweepy.Cursor(twitter_v1.get_friends).items(200):
        # print(friend.screen_name)
        friends.append(friend)
        print(len(friends))
        

    
    # print(len(friends))
    return friends