#!/usr/bin/env python

#InvertedIndex.py

import collections
from Parser import Parser
from tfidf import TFIDF


STOPWORDS_FILE = "stopWords.txt"

class InvertedIndex:


    def __init__(self):
        self.inverted_index = {}
        self.collections_index = {}
        self.unique_id = 0  # for assigning doc ID to docs held in the collections index
        self.parser = Parser()
        self.tfidf = {} 

    '''
    # doc_name == url
    # doc_text == stripped of html
    '''
    def addDocument(self, doc_name, doc_text):

        # split the doc_text into a list of words as they appear in the document
        input_text = doc_text.strip().split()

        # get the twenty words & store the doc in the collections
        twenty_words = self.extractTwentyWords(input_text)
        self.addToCollectionsIndex(doc_name, twenty_words)

        # remove stopWords, to lower case, clean punctuation symbols, and stem
        parsedWords = self.parser.fullParse(input_text)

        # store words in index
        self.addWordsToInvertedIndex(parsedWords)

        # this is the main starting function of the tfidf class
        # self.unique_id -- at this point -- is equivalent to len(collections_index)
        self.calcTFIDF()

    def calcTFIDF(self):
        t = TFIDF()
        self.tfidf = t.docHandler(self.inverted_index, self.unique_id)

 
    
    def extractTwentyWords(self, words_list):
        twenty_words = ''
        for i in range(20):
            twenty_words += words_list[i]
            if (i < 19):
                twenty_words += ' '
        return twenty_words

    def addToCollectionsIndex(self, doc_name, twenty_words):
        self.collections_index[self.unique_id] = [doc_name, twenty_words]
        self.unique_id += 1

    def addWordsToInvertedIndex(self, words_list):
        for word in words_list:
            self.inverted_index[word] = self.inverted_index.get(word, {})
            if not self.inverted_index[word] or self.unique_id not in self.inverted_index[word]:  # if empty list
                self.inverted_index[word][self.unique_id] = 1
            elif self.unique_id in self.inverted_index[word]:
                self.inverted_index[word][self.unique_id] += 1

    def printCollectionsIndex(self):
        print "****************************************************************"
        print "                     COLLECTIONS INDEX"
        print "****************************************************************"
        for key, value in self.collections_index.iteritems():
            print key, value

    def printInvertedIndex(self):
        print "****************************************************************"
        print "                      INVERTED INDEX"
        print "****************************************************************"
        for key, value in self.inverted_index.iteritems():
            print key, value


