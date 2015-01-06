# -*- coding: utf-8 -*-
try:
    from urllib import urlencode
    from urllib2 import urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen

from bs4 import BeautifulSoup


#set your app id here
#http://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html
appid = 'your app id'
pageurl = "http://jlp.yahooapis.jp/MAService/V1/parse"


def split(sentence, appid=appid, results="ma", filter_="1|2|3|4|5|9|10"):
    sentence = sentence.encode('utf-8')
    params = urlencode({'appid': appid,
                        'results': results,
                        'filter': filter_,
                        'sentence': sentence})
    results = urlopen(pageurl, params)
    soup = BeautifulSoup(results.read())

    return [w.surface.string for w in soup.ma_result.word_list]
