

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

