# -*- coding: utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup

from config import Config


config = Config('settings.cfg', 'YAHOO')

pageurl = "http://jlp.yahooapis.jp/MAService/V1/parse"

results = "ma"
filter_ = "1|2|3|4|5|9|10"

def split(sentence):
    params = urlencode({'appid': config.appid,
                        'results': results,
                        'filter': filter_,
                        'sentence': sentence})
    params = bytes(params, encoding='utf-8')

    responce = urlopen(pageurl, params)
    soup = BeautifulSoup(responce.read(), "lxml")

    return [w.surface.string for w in soup.ma_result.word_list]
