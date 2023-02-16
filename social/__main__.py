from rich import print
from datetime import datetime, timezone
# from convert import *
from dateutil import parser  #  pip install python-dateutil --upgrade
import os
import tweepy
import openai
import praw

# environ must be loaded before rivertils
import dotenv
dotenv.load_dotenv(override=True)

from rivertils.rivertils import get_test_message_and_language
import random
import argparse

print("Running social.py")

parser = argparse.ArgumentParser()
parser.add_argument('--test', "-t", action=argparse.BooleanOptionalAction)
parser.add_argument("-c", "--count", help="number of tweets to fetch", type=int, default=25)
parser.add_argument("-p", "--platform", help="which routine to run", type=str, choices=["twitter", "reddit", "insta"], default="twitter")

args = parser.parse_args()
test = args.test
count = args.count
platform = args.platform

if test:
    print("TESTING MODE")
else:
    print("LIVE MODE")

# twitter_yoda = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Yoda. Make it funny."
# twitter_spicoli = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Spicoli from Fast Times at Ridgemont High. Make it funny."
# twitter_gollum = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Gollum from The Hobbit. Make it funny."
# twitter_santa= "respond to this twitter mention as if you are Rivers Cuomo from Weezer mixed with Santa Claus. Make it funny."
# twitter_prompts = [twitter_prompt, twitter_yoda, twitter_spicoli, twitter_gollum]

character = input("which character do you want to use? (default is 'Rivers Cuomo from Weezer')") or "Rivers Cuomo from Weezer"
emotion = input("what emotion do you want the bot to have? (default is 'funny')") or "funny"

# get the last context from the text file
with open("social/last_context.txt", "r") as f:
    last_context = f.read()

context = input(f"any additional context you wish to give the bot about itself? (for example, '{last_context}')") or ""

if context != "":

    # save the ids of the tweet to a text file
    with open("last_context.txt", "w") as f:

        f.write(context)

base_prompt = f"respond to this {platform} comment as if you are {character}. Your response should use current slang and should be {emotion}."
twitter_prompts = [base_prompt]

# will ignore any input containing these words
bads = os.environ.get("BADS").split(",")
print("bads: ", bads)


def build_openai_response(text: str, prompt: str):

    prompt = f"{prompt}.\nHere is the text I want you to respond to: '{text}'"
    # print(prompt)

    reply = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=120,
    )
    reply = reply["choices"]
    reply = reply[0]["text"]
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    reply = reply.replace("2020", "2023")
    reply = reply.replace("2021", "2023")
    reply = reply.strip()
    # print(reply)
    return reply


def sub(s):
    bads = [
        # "@RiversCuomo", 
        # "@Weezer", 
        
        "GenZ",
        "Gen-Z",
     ]
    goods = ["lit", "based"]
    for b in bads:
        s = s.replace(b,random.choice(goods))
    return s


def finalize_response(response: str, language: str):
    """
    Returns a string.
    Replace any names with the user's name. Translate the reponse to the user's language of choice. Append punctuation.
    """

    # if language and language != "en":
    #     blob = TextBlob(response)
    #     # print(blob)

    #     try:
    #         response = blob.translate(to=language).raw
    #     except Exception as e:
    #         print("Couldn't do blob.translate in finalize_reponse: ", e, blob)


    # if language and language != "en":
    #     blob = TextBlob(response)
    #     # print(blob)

    #     try:
    #         response = blob.translate(to=language).raw
    #     except Exception as e:
    #         print("Couldn't do blob.translate in finalize_reponse: ", e, blob)

    # print(response)
    response = response.replace("!", ".")

    # response = sub(response)

    response = remove_continuation_of_previous_tweet(response)

    if len(response) < 1:
        return ""

    # # APPEND PUNCTUATION IF NECESSARY
    # response = append_punctuation(response)
    # # print(response)

    # # Mention the original poster
    # # 5 in 6 chance
    # # # Unless this is a coaching channel
    # # if not active_channel == current_user.username:
    # response = mention(nick, response)

    return response


def is_bad(test_tweet):
    if b := next((b for b in bads if b in test_tweet.lower()), None):
        print("bad tweet: ", b, test_tweet)

    return 


def remove_continuation_of_previous_tweet(reply):
    """ in some cases openai will continue the previous tweet. This function removes that. """
    
    if "\n" not in reply:
        # print("no newline in reply")
        return reply

    elems = reply.split("\n")
    # elem0 = elems[0]
    # if not elem0.startswith(" - ") and not elem0.startswith(".") and len(elem0) >= 11:
    #     # print("elem0 doesn't start with - or . and it's length is greater than 11 so this must be a new tweet rather than a continuation of a response")
    #     return reply
    # print(f"deleting: {elems[0]}")
    # 

    """ assuming the actual response has no newlines """
    bad = "\n".join(elems[:-1])
    print(f"deleting: <{bad}>")
    return reply.replace(bad, "")


def reddit_routine():

    REDDIT_CLIENT_ID =os.environ.get("REDDIT_CLIENT_ID")
    REDDIT_SECRET =os.environ.get("REDDIT_SECRET")
    REDDIT_PASSWORD =os.environ.get("REDDIT_PASSWORD")
    REDDIT_USERNAME =os.environ.get("REDDIT_USERNAME")

    reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="riverbot",
    password=REDDIT_PASSWORD,
    username = REDDIT_USERNAME
    )
    # assume you have a praw.Reddit instance bound to variable `reddit`
    subreddit = reddit.subreddit("weezer")

    # assume you have a Subreddit instance bound to variable `subreddit`
    for i, submission in enumerate(subreddit.hot(limit=count), start=1):
        print("\n")
        print(i, submission.title, submission.score, submission.id)

        # https://praw.readthedocs.io/en/stable/code_overview/models/submission.html

        title = submission.title
        text = submission.selftext

        # print(title, text)
                
        # submission = reddit.submission("39zje0")
        submission.comment_sort = "new"
        top_level_comments = list(submission.comments)
        # print(top_level_comments)

        context = ""
        for comment in top_level_comments[:3]:
            # print(vars(comment))
            body = comment.body.replace("\n", "")
            context += body + "\n"

            test_message, language = get_test_message_and_language(context)

            reply = build_openai_response(context, base_prompt)   
            reply = finalize_response(reply, language)
        

        print(context)
        print("------------------->", end=" ")
        print(reply)


def insta_routine():
    from instagrapi import Client
    from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag

    INSTA_USERNAME = os.environ.get("INSTA_USERNAME")
    INSTA_PASSWORD = os.environ.get("INSTA_PASSWORD")
    INSTA_PK = os.environ.get("INSTA_PK")

    client = Client()
    client.login(INSTA_USERNAME, INSTA_PASSWORD)

    medias = client.user_medias(INSTA_PK, amount=count)
    # print(medias)
    for i, media in enumerate(medias):

        """
        I could get all the comments.
        Then get all the users for each comment.
        Then sort by is_verified or by follower count.
        """
        
        comments=client.media_comments( media.pk, amount=1)
        # print([x.text for x in comments])

        first_comment = comments[0]

        t = first_comment.text
        u = first_comment.user.dict()["username"]

        print(f"({i}): <@{u} > '{t}'")

        test_message, language = get_test_message_and_language(t)

        reply = None

        reply = build_openai_response(t, base_prompt)   
        reply = finalize_response(reply, language)
        reply = f"@{u} {reply}"
        print(f"'{reply}'")
        print("\n")        

        

        if not test:

            # ask for approval
            approved = input("approve? (y/n) ")

            if approved.lower() == "y":
                
                try:
                    # post the reply to insta
                    client.media_comment(media.pk, reply)
                except Exception as e:
                    print(e)


def twitter_routine():

    TWITTER_APP_KEY = os.environ.get("TWITTER_APP_KEY")
    TWITTER_APP_SECRET = os.environ.get("TWITTER_APP_SECRET")

    # TWITTER_v1
    TWITTER_OAUTH_TOKEN = os.environ.get("TWITTER_OAUTH_TOKEN")
    TWITTER_OAUTH_TOKEN_SECRET = os.environ.get("TWITTER_OAUTH_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
    auth.set_access_token(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)
    twitter_v1 = tweepy.API(auth, wait_on_rate_limit=True)

    # get the list of previous tweets from the text file
    with open("social/tweet_ids.txt", "r") as f:
        previous_tweets = f.read().splitlines()    

    tweets_info = twitter_v1.mentions_timeline( count=count)

    for i, tweet in enumerate(tweets_info , start=1):

        if str(tweet.id) in previous_tweets:
            continue

        text = tweet.text
        
        if is_bad(text):
            
            continue

        username = tweet.user.screen_name

        print(f"{i}: <@{username}> '{text}'")

        test_message, language = get_test_message_and_language(text)

        reply = None

        prompt = random.choice(twitter_prompts)

        # every 4 items, add any additional context to the prompt
        if i % 4 == 0:
            prompt += f" Your response could mention the fact that {context}" 
            # print(prompt)

        reply = build_openai_response(text, prompt)   
        reply = finalize_response(reply, language)
        # reply = "test"
        reply = f"@{username} {reply}"
        if len(reply) > 280:
            # print(f"reply too long: {len(reply)}")
            reply = reply[:280]
            continue
        print(f"'{reply}'")
        print("\n")

        if not test:

            # ask for approval
            approved = input("approve? (y)es / (n)o / i(gnore this tweet always)) ")

            if approved.lower() == "y":
                
                # post the reply to twitter
                twitter_v1.update_status(reply, in_reply_to_status_id =tweet.id)

            if approved.lower() in ["i", "y"]:

                # save the ids of the tweet to a text file
                with open("tweet_ids.txt", "a") as f:

                    f.write(str(tweet.id) + "\n")


def main():
    print(platform)

    if platform == "twitter":
        twitter_routine()
    elif platform == "reddit":
        reddit_routine()
    elif platform == "insta":
        insta_routine()



if __name__ == "__main__":
    main()