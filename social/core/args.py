import argparse



def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', "-t", action=argparse.BooleanOptionalAction)
    # parser.add_argument("-c", "--count", help="number of tweets to fetch", type=int, default=25)
    parser.add_argument("-m", "--mode", help="which routine to run", type=str, choices=["twittermentions", "twittertimeline", "reddit", "insta"], default="twittermentions")

    args = parser.parse_args()
    test = args.test
    # count = args.count
    mode = args.mode

    if test:
        print("TESTING MODE")

    else:
        print("LIVE MODE")

    return args

args = get_args()