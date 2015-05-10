# -*- coding: utf-8 -*-

import numpy as np

from naivebayes import NaiveBayes
from twitter_reader import get_tweets


class CrossValidation(object):
    def __init__(self):
        self.classifier = NaiveBayes()

    def create_data(self, user_ids):
        data = []
        for category, ids in user_ids.items():
            tweets = get_tweets(ids)
            categories = [category] * len(tweets)
            data += list(zip(tweets, categories))

        np.random.shuffle(data)
        return data

    def split(self, data, test_percentage):
        n_test = int(len(data)*test_percentage)
        n_training = len(data)-n_test

        # unzip (inverse of zip)
        training = zip(*data[:n_training])
        test = zip(*data[n_training:])
        return training, test

    def show_tweets_with_labels(self, tweets, labels):
        for tweet, label in zip(tweets, labels):
            print("{}:\n{}\n".format(label, tweet))

    def evaluate(self, user_ids, test_percentage=0.2, verbose=True):
        """
        user_ids: Twitter IDs separated into categories.
        test_percentage: Ratio of the amount of test data extracted
        from tweets.
        """

        if not(0 <= test_percentage <= 1):
            raise ValueError("test_percentage must be between 0 and 1 "
                             "(inclusive).")

        data = self.create_data(user_ids)
        training, test = self.split(data, test_percentage)

        tweets, categories = training
        self.classifier.fit(tweets, categories)

        tweets, answers = test
        results = self.classifier.predict(tweets)

        if(verbose):
            self.show_tweets_with_labels(tweets, results)

        return results, answers


class ClassificationResultEvaluator(object):
    def __init__(self, results, answers):
        self.labels = list(np.unique(answers))
        self.results = np.asarray(results)
        self.answers = np.asarray(answers)

    def count_n_true_positives(self, target_label):
        n_true_positives = 0
        for result, answer in zip(self.results, self.answers):
            if(result == answer == target_label):
                n_true_positives += 1
        return n_true_positives

    def calc_accuracy(self):
        n_correct_answers = np.count_nonzero(self.results == self.answers)
        return n_correct_answers / len(self.answers)

    def calc_precision_recall_fmeasure(self, target_label):
        true_positive = self.count_n_true_positives(target_label)

        n_retrieved = np.count_nonzero(self.results == target_label)
        n_relevant = np.count_nonzero(self.answers == target_label)

        precision = true_positive / n_retrieved
        recall = true_positive / n_relevant
        fmeasure = 2 * precision * recall / (precision + recall)
        return precision, recall, fmeasure

    def report(self):
        max_label_length = max(map(len, self.labels))
        white_spaces = ' ' * max_label_length
        print("{}  precision  recall  fmeasure".format(white_spaces))
        format_ = "{:" + str(max_label_length) + "}      "\
                  "{:.3f}   {:.3f}     {:.3f}"

        for target_label in self.labels:
            t = self.calc_precision_recall_fmeasure(target_label)
            precision, recall, fmeasure = t
            print(format_.format(target_label, precision, recall, fmeasure))
        print("\naccuracy: {}\n".format(self.calc_accuracy()))


if(__name__ == '__main__'):

    from config import Config
    config = Config('settings.cfg', 'TWITTER')

    validator = CrossValidation()
    results, answers = validator.evaluate({
        config.true_target_name: config.true_accounts,
        config.false_target_name: config.false_accounts
    })

    evaluator = ClassificationResultEvaluator(results, answers)
    evaluator.calc_accuracy()
    evaluator.report()
