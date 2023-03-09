

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

