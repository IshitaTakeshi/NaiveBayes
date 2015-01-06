from __future__ import division

import json
import math
import sys

import splitter


class NaiveBayes():
    def __init__(self):
        self.vocabularies = set()
        self.word_count = {}  # {category1: {word1: 4, word2: 2,...}, ... }
        self.category_count = {}  # {category1: 16, category2: 4 ...}

    def count_word(self, word, category):
        self.word_count.setdefault(category, {})
        self.word_count[category].setdefault(word, 0)
        self.word_count[category][word] += 1
        self.vocabularies.add(word)

    def count_category(self, category):
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def fit(self, doc, category):
        words = splitter.split(doc)
        for word in words:
            self.count_word(word, category)
        self.count_category(category)

    def calc_category_frequency(self, category):
        #calc log(P(cat))
        total_occurrences_of_category = sum(self.category_count.values())
        n_docs_in_category = self.category_count[category]
        return n_docs_in_category / total_occurrences_of_category

    def get_n_occurrences_of_word(self, word, category):
        if(word in self.word_count[category]):
            return self.word_count[category][word]
        return 0

    def calc_word_frequency(self, word, category):
        #calc P(word_i|cat)
        numerator = self.get_n_occurrences_of_word(word, category) + 1
        #sum occurrence of words in the category
        n_words_in_category = sum(self.word_count[category].values())
        denominator = n_words_in_category + len(self.vocabularies)
        probability = numerator / denominator
        return probability

    def calc_score(self, words, category):
        #calc log(P(cat|doc)) = log(P(cat)) + sum_i{log(P(word_i|cat))}
        score = math.log(self.calc_category_frequency(category))
        for word in words:
            score += math.log(self.calc_word_frequency(word, category))
        return score

    def predict(self, doc):
        #arg max log(P(cat|doc))
        best_guessted_category = None
        max_probability = -float('inf')
        words = splitter.split(doc)

        for category in self.category_count.keys():
            probability = self.calc_score(words, category)
            if(probability > max_probability):
                max_probability = probability
                best_guessted_category = category
        return best_guessted_category

    def dump_json(self, filename):
        attributes = self.__dict__
        attributes['vocabularies'] = list(attributes['vocabularies'])
        json.dump(attributes, open(filename, 'w'))

    def load_json(self, filename):
        attributes = json.load(open(filename, 'r'))
        attributes['vocabularies'] = set(attributes['vocabularies'])
        self.__dict__ = attributes
