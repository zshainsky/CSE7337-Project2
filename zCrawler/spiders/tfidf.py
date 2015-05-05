#!/usr/bin/env python

"""
https://github.com/hrs/python-tf-idf/blob/master/tfidf.py
The simplest TF-IDF library imaginable.
Add your documents as two-element lists `[docname, [list_of_words_in_the_document]]` with `addDocument(docname, list_of_words)`. Get a list of all the `[docname, similarity_score]` pairs relative to a document by calling `similarities([list_of_words])`.
See the README for a usage example.

"""

import sys
import os
import operator
import numpy as np
import matplotlib.pyplot as plt
import io
import csv

RESULTS_DIRECTORY = "CrawlerResults"

class tfidf:
  def __init__(self):
    self.weighted = False
    self.documents = []
    self.corpus_dict = {}
    self.top20_x = []
    self.top20_y = []
    self.top20_w = []
    self.top20 = []

  def addDocument(self, doc_name, list_of_words):
    # building a dictionary
    doc_dict = {}
    for word in list_of_words:
      doc_dict[word] = doc_dict.get(word, 0.) + 1.0
      
      #Generates the Corpus with a dictionary containing [document frequency, term frequency] as the value of each key
      self.corpus_dict[word] = self.corpus_dict.get(word, [0,0])
      self.corpus_dict[word][0] += 1

    for word in doc_dict:
      self.corpus_dict[word][1] +=1

    # normalizing the dictionary
    length = float(len(list_of_words))
    for k in doc_dict:
      doc_dict[k] = doc_dict[k]

    # add the normalized document to the corpus
    self.documents.append([doc_name, doc_dict])


  def generateDocFrequency(self, list_of_words):
    """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

    # computing the list of similarities
    sims = []
    temp_dict = {}
    for doc in self.documents:
      score = 0.0
      #get the array of terms
      doc_dict = doc[1]
      for k in doc_dict:
        if self.corpus_dict.has_key(k):
          #[doc freq, term freq]
          self.corpus_dict.get(k)[0] += 1


  def generateCorpusTable(self):
    temp = sorted(self.corpus_dict.items(), key=operator.itemgetter(1), reverse=True)
    self.top20_x = []
    self.top20_y = []
    

  def printCorpusTable(self):
    temp = sorted(self.corpus_dict.items(), key=operator.itemgetter(1), reverse=True)
    print "CORPUS TABLE:", temp, "  LENGTH:  ", len(temp)
    for index in range(0,20):
       print temp[index]

  def outputCorpusTable(self):
    temp = sorted(self.corpus_dict.items(), key=operator.itemgetter(1), reverse=True)
    with io.open(RESULTS_DIRECTORY + '/Corpus.txt', 'w', encoding='utf-8') as f:
      for word in temp:
        for index in range(0,len(temp)):
          f.write(str(temp[index]).strip(unicode( () ) ))
          f.write(unicode("\n"))

  def outputTop20Words(self):
    #self.top20 = []
    self.top20_x = []
    self.top20_y = []
    temp = sorted(self.corpus_dict.items(), key=operator.itemgetter(1), reverse=True)
    with io.open(RESULTS_DIRECTORY + '/Top20Words.txt', 'w', encoding='utf-8') as f:
      for index in range(0, 20):
      #for item in self.top20_w:
        #self.top20.append(temp[index])
        self.top20_x.append(temp[index][1][0])
        self.top20_y.append(temp[index][1][1])
        f.write(str(temp[index]).strip(unicode( () ) ) ) 
        f.write(unicode('\n'))


  def graphTop20(self):
    x = self.top20_x
    y = self.top20_y
    plt.title("20 Most Frequently Occurring Words", fontsize=20)
    plt.ylabel('Word Frequency', fontsize=16)
    plt.xlabel('Document Frequency', fontsize=16)
    plt.scatter(x, y)
    plt.savefig(RESULTS_DIRECTORY + '/top20.pdf', bbox_inches='tight')


