from social.core import config

def is_bad(test_tweet):
    if b := next((b for b in config.bads if b in test_tweet.lower()), None):
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


