# -*- coding: utf-8 -*-


import sys
import json
import time

import numpy as np

from naivebayes import NaiveBayes
from twitter_reader import get_tweets


class Classifier(object):
    def __init__(self):
        self.classifier = NaiveBayes()

    def learn_from_tweets(self, user_ids, category):
        tweets = get_tweets(user_ids)
        categories = [category] * len(tweets)
        self.classifier.fit(tweets, categories)
        print("Training...")

    def predict_user_input(self):
        """Read user input until 'exit' is entered"""
        sentence = input("input =>")
        while(sentence != 'exit'):
            category = self.classifier.predict_(sentence)
            print("category: {}".format(category))
            sentence = input("input =>")

    def save(self, filename):
        self.classifier.dump_json(filename)

    def load(self, filename):
        self.classifier.load_json(filename)


if(__name__ == '__main__'):
    classifier = Classifier()

    if(len(sys.argv) >= 2):
        # load classifier settings and params
        classifier.load(sys.argv[1])
        classifier.predict_user_input()
        exit(0)

    from config import Config

    config = Config('settings.cfg', 'TWITTER')
    classifier.learn_from_tweets(
        config.true_accounts,
        config.true_target_name
    )

    classifier.learn_from_tweets(
        config.false_accounts,
        config.false_target_name
    )

    # save the classifier parameters
    classifier.save('result.json')
    classifier.predict_user_input()
