import sys
import codecs

import twitter

from config import Config

config = Config('settings.cfg', 'TWITTER')


auth = twitter.OAuth(
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    token=config.token,
    token_secret=config.token_secret
)

api = twitter.Twitter(auth=auth)


def get_tweets(accounts):
    """Get recent 200 tweets from each account"""

    def get_tweets_(screen_name):
        statuses = api.statuses.user_timeline(screen_name=screen_name,
                                              count=200)
        return [s['text'] for s in statuses]

    tweets = []
    for account in accounts:
        tweets += get_tweets_(account)
    return tweets
