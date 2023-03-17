import openai
import random
import os

from social.twitter.helpers import remove_continuation_of_previous_tweet


def build_openai_response(text: str, prompt: str):

    prompt = f"{prompt}.\nHere is the text I want you to respond to: '{text}'"

    # Get the open model from .env if the user has specified it.
    model = os.environ.get("OPENAI_MODEL")

    # Use gpt-3 if the model is not specified
    if model is None:
        model = "text-davinci-003"

    # Use gpt-4 if the model is specified as gpt-4
    if model == "gpt-4":

        completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
        reply = completion.choices[0].message.content    

    # Otherwise use gpt-3 or another model specified in .env
    else:
        completion = openai.Completion.create(
            model=os.environ.get("OPENAI_MODEL"),
            prompt=prompt,
            temperature=1,
            max_tokens=120,
        )
        reply = completion["choices"]
        reply = reply[0]["text"]

    # whatever the model was, now you can make a few universal changes to the response.
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    reply = reply.replace("2020", "2023")
    reply = reply.replace("2021", "2023")
    reply = reply.strip()
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
