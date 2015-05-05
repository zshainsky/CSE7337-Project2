#!/usr/bin/env python

#InvertedIndex.py

import collections
from porterStemmer import PorterStemmer
import re, string
from string import maketrans
from Translator import Translator

STOPWORDS_FILE = "stopWords.txt"

class InvertedIndex:

    def __init__(self):
        self.inverted_index = {}
        self.collections_index = {}
        self.stemmer = PorterStemmer()
        self.unique_id = 0  # for assigning doc ID to docs held in the collections index
        self.remove_punctuation_set = set('!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
        self.stopWordsList = []
        self.loadStopWords()

    # doc_name == url
    # doc_text == stripped of html
    def addDocument(self, doc_name, doc_text):

        # split the doc_text into a list of words as they appear in the document
        input_text = doc_text.strip().split()

        # get the twenty words & store the doc in the collections
        twenty_words = self.extractTwentyWords(input_text)
        self.addToCollectionsIndex(doc_name, twenty_words)

        # remove stop words
        stopped_list = self.removeStopWords(input_text)

        # remove case and punctuation
        words = self.cleanCaseAndPunctuation(stopped_list)

        #stem words
        stemmed_words = self.stemWords(words)

        #store words in index
        self.addWordsToInvertedIndex(stemmed_words)

    def stemWords(self, words_list):
        stemmed = []
        for word in words_list:
            word = self.stemmer.stem(word, 0, len(word)-1)
            stemmed.append(word)
        return stemmed

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


    def removeStopWords(self, words_list):
        non_stop_list = []
        for word in words_list:
            word = ''.join(filter(lambda word: word not in self.stopWordsList, word.strip()))
            non_stop_list.append(word)
        return non_stop_list

    def cleanCaseAndPunctuation(self, words_list):
        clean_list = []
        for word in words_list:
            word = word.lower()
            if not word.startswith('http'):
                clean = ''.join([c for c in word if c not in self.remove_punctuation_set])
                if clean:
                    clean_list.append(clean)
        return clean_list

    def loadStopWords(self):
        for line in open(STOPWORDS_FILE):
            self.stopWordsList.append(line.strip())
            #self.forbidden_words = set(stopWordsList)

    def printStopWords(self):
        print "****************************************************************"
        print "                         STOP WORDS"
        print "****************************************************************"
        print self.stopWordsList

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


