# -*- coding: utf-8 -*-

from __future__ import division

import json
import math
import sys

import splitter


class NaiveBayes(object):
    def __init__(self):
        self.vocabulary = set()  # 出現した単語の種類全部
        self.word_count = {}  # {category1: {word1: 4, word2: 2,...}, ... }

        self.alpha = 0.01  # 加算スムージングのパラメータ

    def count_word(self, word, category):
        """
        ある単語が出現した回数をカテゴリごとに数える。
        たとえば、政治カテゴリの中で「内閣」という単語が出現したら、
        政治カテゴリの「内閣」の出現回数を1増やす。
        """
        self.word_count.setdefault(category, {})
        self.word_count[category].setdefault(word, 0)
        self.word_count[category][word] += 1
        self.vocabulary.add(word)

    def fit(self, sentences, categories):
        assert(len(sentences) == len(categories))

        for sentence, category in zip(sentences, categories):
            self.fit_(sentence, category)

    def fit_(self, sentence, category):
        words = splitter.split(sentence)
        for word in words:
            self.count_word(word, category)

    def calc_category_frequency(self, category):
        """
        カテゴリが`category`である文書が，入力された文書全体のうち
        どれだけの割合を占めるかを計算する。
        """

        # 学習データ内に含まれる全ての単語の数
        n_total_words = 0
        for category in self.word_count.keys():
            n_total_words += sum(self.word_count[category].values())

        # あるカテゴリ内の単語の総数
        n_words_in_category = sum(self.word_count[category].values())
        return n_words_in_category / n_total_words

    def calc_word_frequency(self, word, category):
        """
        カテゴリ`category`内で単語`word`が出現する確率
        P(`word`|`category`) を計算する。
        """
        # カテゴリが`category`である文書全体の中での単語`word`の出現回数
        # `word`が文書内に存在しない場合は0
        word_occurences = self.word_count[category].get(word, 0)

        # カテゴリ`category`内の全単語数
        # 同じ単語が`category`内に複数回現れる場合はその回数ぶんを加算する。
        n_words_in_category = sum(self.word_count[category].values())

        # 単語の種類の数
        V = len(self.vocabulary)

        # 本来は
        # `probability = word_occurences/n_words_in_category`
        # で計算できるが、`category`内に存在しない単語が入力されると
        # `probability`が0になってしまうため、
        # `probability = (word_occurences + 1)/ (n_words_in_category + V)`
        # としている(ゼロ頻度問題)。
        probability = (word_occurences + 1) / (n_words_in_category + V)
        return probability

    def calc_score(self, words, category):
        # P(category|sentence) is proportional to
        # P(category)P(sentence| category)
        # = P(category)prod_i{P(word_i|category)}
        # log(P(category|sentence)) is proportional to
        # log(P(category)) + sum_i{log(P(word_i|category))}

        # log(P(category))
        score = math.log(self.calc_category_frequency(category))

        # sum_i{log(P(word_i|category))}
        for word in words:
            score += math.log(self.calc_word_frequency(word, category))
        return score

    def predict(self, sentences):
        categories = []
        for sentence in sentences:
            category = self.predict_(sentence)
            categories.append(category)
        return categories

    def predict_(self, sentence):
        # arg max log(P(category| sentence))
        best_suggested_category = None
        max_probability = -float('inf')
        words = splitter.split(sentence)

        for category in self.word_count.keys():
            probability = self.calc_score(words, category)
            if(probability > max_probability):
                max_probability = probability
                best_suggested_category = category
        return best_suggested_category

    def dump_json(self, filename):
        attributes = self.__dict__
        # setはそのままdumpできないのでlistに変換
        attributes['vocabulary'] = list(attributes['vocabulary'])
        json.dump(attributes, open(filename, 'w'))

    def load_json(self, filename):
        attributes = json.load(open(filename, 'r'))
        attributes['vocabulary'] = set(attributes['vocabulary'])
        self.__dict__ = attributes
