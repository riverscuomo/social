from rich import print
from datetime import datetime, timezone
import social.data.test_tweets as test_tweets
from dateutil import parser  #  pip install python-dateutil --upgrade
import os
from insta import insta
from twitter import routine as twitter
from reddit import reddit
from social.core import config



import praw

# environ must be loaded before rivertils
from dotenv import load_dotenv
load_dotenv(override=True)


import random
print("Running social.py")
from social.core.args import args




def main():
    if args.mode in ["twittermentions", "twittertimeline"]:
        twitter.routine(args.mode)
    elif args.mode == "reddit":
        reddit.reddit_routine()
    elif args.mode == "insta":
        insta.insta_routine()


if __name__ == "__main__":
    main()

