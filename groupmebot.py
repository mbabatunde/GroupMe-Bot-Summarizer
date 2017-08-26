#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re

from timeit import default_timer
from groupy import Group, Bot, Member

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

__author__ = "Mark Babatunde"

COUNT = 0

def groupme_bot():
    sentenceList = []
    group = Group.list().first
    messages = group.messages()
    message = str(messages.newest)

    regex = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})"
    #regex = r"(\s*(.+?)(?:\s+(\d+)(?:(?:\s+\(?of\s+|-)(\d+)\)?)?)?|(\w+)): (https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-ZA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})"
    
    bot = Bot.list().first

    LANGUAGE = "english"
    SENTENCES_COUNT = 2

    matches = re.finditer(regex, message)

    bot.post("Beginning the TL;DR summary:")
    for matchNum, match in enumerate(matches):
        matchNum += 1
        url = str(match.group(1))
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        start = default_timer()

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            sentenceList.append(str(sentence))
    
    print (sentenceList)
    bot.post(str(sentenceList).replace("[","").replace("]","").replace("'","").replace("\\n"," "))
    duration = default_timer() - start
    bot.post("Time to complete this TL;DR summary: " + '{:.2f}'.format(float(duration)) + " seconds")
    print("Successfully completed!")
    
if __name__=="__main__":
    groupme_bot()

