# from social.core.args import args
from social.twitter import helpers
from social.twitter.service_v1 import get_twitter_vi
from social.twitter import timeline
from social.core import response
from social.data import test_tweets
# environ must be loaded before rivertils
from dotenv import load_dotenv
load_dotenv(override=True)
from rivertils import rivertils

import random

def routine(args, prompts, last_context, bads):  
    """ Both twittermentions and twittertimeline are handled here. """
    

    twitter_v1 = get_twitter_vi()

    # t  = get_full_text(1627275021961011201, twitter_v1)
    # print(t)
    # exit()



    # get the list of previous tweets from the text file
    with open("social/tweet_ids.txt", "r") as f:
        previous_tweets = f.read().splitlines()    

    # get the list of previous tweets from the text file
    with open("social/bad_users.txt", "r") as f:
        bad_users = f.read().splitlines() 
    print("bad_users", bad_users)


    # timeline = twitter_v1.home_timeline( )

    # for status in tweepy.Cursor(twitter_v1.home_timeline, "Tweepy",
    #     count=200).items():
    #     print(status.id)

    # timeline_tweets 
    # # timeline_tweets = fetch_timeline_tweets(twitter_v1)
    # print(f"timeline_tweets: {len(timeline_tweets)}")


    if args.mode == "twittermentions":
        tweets = twitter_v1.mentions_timeline(tweet_mode="extended", count=200 )
        tweets.sort(key=lambda x: x.user.followers_count, reverse=True)

    elif args.mode == "twittertimeline":
        tweets = test_tweets.test_tweets if args.test else timeline.fetch_timeline_tweets(twitter_v1)
        tweets.sort(key=lambda x: x.retweet_count + x.favorite_count, reverse=True)

    else:
        raise Exception("invalid mode")

    
    tweets = [x for x in tweets if x.id_str not in previous_tweets]
    tweets = [x for x in tweets if not helpers.is_bad(x.full_text, bads) ]
    tweets = [x for x in tweets if x.favorite_count!=0 ]
    tweets = [x for x in tweets if str(x.user.id) not in bad_users ]
    


    for i, tweet in enumerate(tweets, start=1):
        # print(tweet)

        # id = tweet.id
        # if id in previous_tweets:
        #     continue
        text = tweet.full_text.replace("\n", " ") 
        # if is_bad(text):
        #     continue

        retweet_count = tweet.retweet_count
        favorite_count = tweet.favorite_count
        # if retweet_count > 150 or favorite_count > 150:
        screen_name = tweet.user.screen_name
        user_id = tweet.user.id
        followers_count = tweet.user.followers_count
        following_count = tweet.user.friends_count
        followers_minus_following = followers_count - following_count
        possibly_sensitive = tweet.possibly_sensitive if hasattr(tweet, "possibly_sensitive") else False
        log = f"{i}: {screen_name} | {text} | (retweets: {retweet_count}, favorites: {favorite_count}, followers: {followers_minus_following}, user_id: {user_id}"
        if possibly_sensitive:
            log += " (possibly sensitive)!!!"
        print(log)
                # print(json)


    # for i, tweet in enumerate(mentions , start=1):

        # if str(tweet.id) in previous_tweets:
        #     continue

        # text = tweet.text

        # if is_bad(text):

            # continue

        username = tweet.user.screen_name

        # print(f"{i}: <@{username}> '{text}'")

        test_message, language = rivertils.get_test_message_and_language(text)

        reply = None

        prompt = random.choice(prompts)

        # every 4 items, add any additional context to the prompt
        if i % 4 == 0:
            prompt += f" Your response could mention the fact that {last_context}" 
            # print(prompt)

        reply = response.build_openai_response(text, prompt)   
        reply = response.finalize_response(reply, language)
        # reply = "test"
        reply = f"@{username} {reply}"
        if len(reply) > 280:
            # print(f"reply too long: {len(reply)}")
            reply = reply[:280]
            continue
        print(f"'{reply}'")
        print("\n")

        if not args.test:

            # ask for approval
            i = input("approve? (y)es / (n)o / i(gnore this tweet always)) ").lower()

            if i == "y":

                # post the reply to twitter
                twitter_v1.update_status(reply, in_reply_to_status_id =tweet.id)
                tweet.favorite()

            if i in ["i", "y"]:

                print('opening tweet_ids to save the id of the tweet')

                # save the ids of the tweet to a text file
                with open("social/tweet_ids.txt", "a") as f:
                    # print(f"writing {tweet.id} to tweet_ids.txt")

                    f.write(str(tweet.id) + "\n")

            elif i == 'q':
                exit()

            elif i == "tt":
                args.mode="twittertimeline"
                routine(args, prompts, last_context, bads)

