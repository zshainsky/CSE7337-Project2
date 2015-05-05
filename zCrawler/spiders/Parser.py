

from porterStemmer import PorterStemmer
import re, string
from string import maketrans

STOPWORDS_FILE = "stopWords.txt"

class Parser:

    def __init__(self):
        self.remove_punctuation_set = set('!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
        self.stemmer = PorterStemmer()
        self.stopWordsList = []
        self.loadStopWords()

    def fullParse(self, words_list):
        stopped = self.removeStopWords(words_list)
        cleaned = self.cleanCaseAndPunctuation(stopped)
        stopped = self.stemWords(cleaned)
        return stopped
        

    '''
    used by self.fullParse function
    '''
    def _removeStopWords(self):
        for word in self.parseWordList:
            word = ''.join(filter(lambda word: word not in self.stopWordsList, word.strip()))

    def _stemWords(self):
        for word in self.parseWordList:
            word = self.stemmer.stem(word, 0, len(word)-1)

    def _cleanCaseAndPunctuation(self):
        for word in self.parseWordList:
            word = word.lower()
            if not word.startswith('http'):
                word = ''.join([c for c in word if c not in self.remove_punctuation_set])
                

    '''
    for external calls
    '''
    def stemWords(self, words_list):
        stemmed = []
        for word in words_list:
            word = self.stemmer.stem(word, 0, len(word)-1)
            stemmed.append(word)
        return stemmed

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

    def printStopWords(self):
        print "****************************************************************"
        print "                         STOP WORDS"
        print "****************************************************************"
        print self.stopWordsList


    '''
    happens on __init__
    '''
    def loadStopWords(self):
        for line in open(STOPWORDS_FILE):
            self.stopWordsList.append(line.strip())
            #self.forbidden_words = set(stopWordsList)

