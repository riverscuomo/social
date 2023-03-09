
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

