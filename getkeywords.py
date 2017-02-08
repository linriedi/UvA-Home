# -*-coding:utf-8-*-
"""Keyword extraction class for the media understanding 2017 project.

https://www.airpair.com/nlp/keyword-extraction-tutorial

File name: test.py
Author: Media Undertanding 2017
Date created: 7/2/2017
Date last modified: 7/2/2017
Python Version: 3.4
"""

import RAKE as r

debug = False

class GetKeyWords():
    def __init__(self, text):
        self.text = text
        self.keys = self.get(text)

    def get(self, text):
        return r.run(self.text)

if debug:
    text = "The long-string instrument is a musical instrument in which the string is of such a length that the ... One example of a long-string instrument was invented by the American composer Ellen Fullman. It is tuned in just intonation and played by"
    keys = GetKeyWords(text)
    print(keys.keys)