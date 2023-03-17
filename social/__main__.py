from rich import print
from datetime import datetime, timezone
import social.data.test_tweets as test_tweets
from dateutil import parser  #  pip install python-dateutil --upgrade
import os
from social.insta import insta
from social.twitter import routine as twitter
from social.reddit import reddit
from social.core import config, get_prompts, get_args
import praw

# environ must be loaded before rivertils
from dotenv import load_dotenv
load_dotenv(override=True)

print("Running social.py")


def main():

    args = get_args.get_args()
    last_context, bads = config.config()    
    prompts = get_prompts.get_prompts(last_context, args)

    if args.mode in ["twittermentions"]:
        twitter.routine(args, prompts, last_context,bads)
    elif args.mode == "twittertimeline":
        twitter.routine(args, prompts, None,bads)
    elif args.mode == "reddit":
        reddit.reddit_routine()
    elif args.mode == "insta":
        insta.insta_routine()


if __name__ == "__main__":

    
    main()

