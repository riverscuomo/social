from social.core import config
from social.core.args import args

def get_prompts():
    character = input("which character do you want to use? (default is 'Rivers Cuomo from Weezer')") or "Rivers Cuomo from Weezer"
    emotion = input("what emotion do you want the bot to have? (default is 'funny')") or "funny"
    context = input(f"any additional context you wish to give the bot about itself? (for example, '{config.last_context}')") or ""
    if context != "":
        config.save_context(context)

    base_prompt = f"respond to this {args.mode} comment as if you are {character}. Your response should use current slang and should be {emotion}."
    # twitter_yoda = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Yoda. Make it funny."
    # twitter_spicoli = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Spicoli from Fast Times at Ridgemont High. Make it funny."
    # twitter_gollum = "respond to this twitter mention as if you are Rivers Cuomo from Weezer, but using the language of Gollum from The Hobbit. Make it funny."
    # twitter_santa= "respond to this twitter mention as if you are Rivers Cuomo from Weezer mixed with Santa Claus. Make it funny."
    # twitter_prompts = [twitter_prompt, twitter_yoda, twitter_spicoli, twitter_gollum]
    prompts = [
        base_prompt,
        ]
    return prompts

prompts = get_prompts()