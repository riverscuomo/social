def config():
    """ return the last context and the bads from text files """

    # get the last context from the text file
    with open("social/last_context.txt", "r") as f:
        last_context = f.read()

    # will ignore any input containing these words
    # get the last context from the text file
    with open("social/bads.txt", "r") as f:
        bads = f.read()
    print("bads: ", bads)
    return last_context, bads

def save_context(context: str):
    """ save the ids of the tweet to a text file """
    with open("social/last_context.txt", "w") as f:
        f.write(context)

# last_context, bads = get_config()

