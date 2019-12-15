"""
Downloads all tweets from a given user.
Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
Twitter doesn't allow retreiving more tweets than this through the API, so we get
as many as possible.
t.py should contain the imported variables.
"""

from __future__ import print_function

import json
import sys
from io import open

import twitter
from t import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=120, exclude_replies=True, include_rts=False)

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, tweet_mode='extended'
    )

    with open("classusers.txt", "r") as file:
        users = file.readlines()
    
    for screen_name in users:
        screen_name = screen_name.strip()
        print(screen_name)
        timeline = get_tweets(api=api, screen_name=screen_name)

        path = 'classtimelines/' + screen_name + '.json'
        with open(path, 'w+') as f:
            for tweet in timeline:
                f.write(json.dumps(tweet._json))
                f.write('\n')