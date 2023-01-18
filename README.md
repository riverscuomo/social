# Social [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

A python package that uses OpenAI to generate a response to a social media mention.

I'm currently just using this for Twitter. Insta replies as a new comment on the post. Reddit works too I think.

See my twitter replies for an example: https://twitter.com/RiversCuomo/with_replies

## Installation

Depending on which of the 3 social media platforms you want to use, you'll register for the appropriate API keys. 

## Environment Variables

You can specify custom variables to include using a `.env` file.  Alternatively, you can set them as Environment Variables.

### API Credentials

OPENAI_API_KEY=x

INSTA_USERNAME=x
INSTA_PASSWORD=x
INSTA_PK=x

REDDIT_CLIENT_ID=x
REDDIT_SECRET=x
REDDIT_PASSWORD=x
REDDIT_USERNAME=x

TWITTER_APP_KEY=x
TWITTER_APP_SECRET=x
TWITTER_OAUTH_TOKEN=x
TWITTER_OAUTH_TOKEN_SECRET=x

### Google Cloud Translate for Language Translation (optional)
GOOGLE_CLOUD_PROJECT=
GOOGLE_APPLICATION_CREDENTIALS=path_to_json_file

### The script will ignore any mentions that contain these words (comma separated)
BADS=xxx,yyy,zzz

## Running

Once you have completed all the installation steps, run `Social` script by running either:

Traditional:

```shell
py -m social
```

Poetry:

```shell
poetry run python -m social
```



