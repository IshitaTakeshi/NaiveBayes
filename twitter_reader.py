import sys
import codecs

import twitter


#set your key here
#https://dev.twitter.com/
api = twitter.Api(
    consumer_key='consumer key',
    consumer_secret='consumer secret',
    access_token_key='token key',
    access_token_secret='token secret'
)


def get_tweets(screen_name):
    statuses = api.GetUserTimeline(screen_name=screen_name, count=200)
    return [s.text for s in statuses]
