from rich import print
# from datetime import datetime, timezone
# import social.data.test_tweets as test_tweets
# from dateutil import parser  #  pip install python-dateutil --upgrade
# import os
# from insta import insta
# from twitter import routine as twitter
# from reddit import reddit
# from social.core import config
from social.twitter.service_v1 import get_twitter_vi
from social.twitter import timeline
from social.twitter import friends

# # environ must be loaded before rivertils
# from dotenv import load_dotenv
# load_dotenv(override=True)


    

def analyze_timeline_for_mutes(twitter_v1):
    """ My theory is that many large accounts are not showing up in my fetch_timeline_tweets() result because I have muted them. """
    print("analyze_timeline_for_mutes")

    tweets=timeline.fetch_timeline_tweets(twitter_v1)
    print(len(tweets))

    for tweet in tweets:
        user = tweet.user


        # print(user._json)
        # exit()
        # print(user.muting, user.screen_name)
        # if user.muting == True:
        #     print(user.screen_name, user.followers_count, end="...")

        #     if user.followers_count > 10000:
        #         print("unmuting")
        #         twitter_v1.destroy_mute(user_id=  user.id)
        #     else:
        #         print("not unmuting")




def main():
    print("Running explore.py")
    twitter_v1 = get_twitter_vi()
    # analyze_timeline_for_mutes(twitter_v1)
    # exit()


    # user= twitter_v1.get_user(screen_name="riverscuomo")
    # friends = user.friends(count=100)

    f = friends.fetch(twitter_v1, "riverscuomo")

    # filter friends where muting is True
    f = [x for x in f if x.muting == True]

    # sort friends by followers count, descending
    f.sort(key=lambda x: x.followers_count, reverse=True)

    # print(friends)
    for friend in f:
        print(friend.screen_name, friend.followers_count, end="...")
        if friend.followers_count > 10000:
            print("unmuting")
            
            # unmute the user
            twitter_v1.destroy_mute(user_id=  friend.id)

    print("\n")
    print(len(f))

if __name__ == "__main__":
    main()


