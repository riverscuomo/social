import tweepy
import os

def get_twitter_vi():
    TWITTER_APP_KEY = os.environ.get("TWITTER_APP_KEY")
    TWITTER_APP_SECRET = os.environ.get("TWITTER_APP_SECRET")

    # TWITTER_v1
    TWITTER_OAUTH_TOKEN = os.environ.get("TWITTER_OAUTH_TOKEN")
    TWITTER_OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_OAUTH_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
    auth.set_access_token(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)
    twitter_v1 = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_v1


