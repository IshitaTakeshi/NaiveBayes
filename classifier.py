import sys
import json
import time

from naivebayes import NaiveBayes
import twitter_reader


def get_tweets(accounts):
    """Get recent 200 tweets from each account"""
    tweets = []
    for account in accounts:
        tweets += twitter_reader.get_tweets(account)
    return tweets


class Classifier(object):
    def __init__(self):
        self.classifier = NaiveBayes()

    def learn_from_tweets(self, user_ids, category):
        print("Training...")
        tweets = get_tweets(user_ids)
        for i, tweet in enumerate(tweets):
            self.classifier.fit(tweet, category)

    def save(self, filename):
        self.classifier.dump_json(filename)

    def load(self, filename):
        self.classifier.load_json(filename)

    def predict_user_input(self):
        """Read user input until 'exit' is entered"""
        text = raw_input("input =>")
        while(text != 'exit'):
            text = text.decode('utf-8')
            category = self.classifier.predict(text)
            print("category: {}".format(category))
            text = raw_input("input =>")


if(__name__ == '__main__'):
    classifier = Classifier()

    #you can load classifier settings and params if the file exists
    #classifier.load('classifier.json')

    classifier.learn_from_tweets(
        [
            'tsundere account id 1',
            'tsundere account id 2',
        ],
        'tsundere'
    )

    classifier.learn_from_tweets(
        [
            'normal account id 1',
            'normal account id 2',
        ],
        'not_tsundere'
    )

    #save classifier parameters
    classifier.save('classifier.json')
    classifier.predict_user_input()
