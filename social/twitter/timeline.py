
def fetch_timeline_tweets(twitter_v1):
    """ Fetches the most popular 50 among the last 800 tweets from the home timeline"""
    timeline_tweets = []
    # https://docs.tweepy.org/en/stable/v1_pagination.html
    # for page in tweepy.Cursor(twitter_v1.home_timeline, tweet_mode="extended",  exclude_replies=True, include_entities=False, count=800).pages(4):
    #     for tweet in page:
    #         json = tweet._json
    #         timeline_tweets.append(json)
    timeline_tweets = twitter_v1.home_timeline(tweet_mode="extended",  exclude_replies=True, include_entities=False, count=200)    
    max_id = timeline_tweets[-1].id
    print(max_id)
    for i in range(4):
        timeline_tweets += twitter_v1.home_timeline(tweet_mode="extended",  exclude_replies=True, include_entities=False, count=200, max_id=max_id)
        max_id = timeline_tweets[-1].id
        print(i, max_id, len(timeline_tweets))

    
    print(len(timeline_tweets))
    return timeline_tweets

