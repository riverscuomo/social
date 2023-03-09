import openai
import random

from social.twitter.helpers import remove_continuation_of_previous_tweet


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
