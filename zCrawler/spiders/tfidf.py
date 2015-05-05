from __future__ import division
from copy import deepcopy
import math


class TFIDF:

    def __init__(self):
        self.numDocs = 0;


    def findNumDocs(self, invIndex):
        numDocs = 0
        for key, value in invIndex.iteritems():
            for k, v in value.iteritems():
                if k > numDocs:
                    numDocs = k
        return numDocs

    def calcDocFrequency(self, invIndex):
        df = {}
        for key, val in invIndex.iteritems():
            df[key] = len(val)
        return df

    def sumTermFrequency(self, invIndex):
        #len(tfSum) is the number of docs
        tfSum = {}
        tempSum = 0
        for key, val in invIndex.iteritems():
            for k, v in val.iteritems():
                temp = tfSum.get(k,-1)
                if temp == -1:
                    tfSum[k] = v
                else:
                    tfSum[k] += v
        return tfSum

    def normalizeTermFrequency(self, invIndex):
        tfSum = self.sumTermFrequency(invIndex)

        #Might need...Thought shallow copy would alter both copies of the data if one was edited
        normalizedIndex = deepcopy(invIndex)
        #normalizedIndex = dict.copy(invIndex)

        for key, value in normalizedIndex.iteritems():
            for k, v in value.iteritems():
                normalizedIndex[key][k] = v/tfSum[k]
        #return new inverted index with normalized term frequency values
        return normalizedIndex

    def calcIDF(self, invIndex):
        df = self.calcDocFrequency(invIndex)
        idf = {}

        for key, value in df.iteritems():
            idf[key] = 1 + math.log10(self.numDocs/df[key])
        return idf


    def calcTF_IDF(self, invIndex):
        normTF = self.normalizeTermFrequency(invIndex)
        idf = self.calcIDF(invIndex)

        tempTF_IDF = {}
        for key, value in normTF.iteritems():
            isTermInKey = tempTF_IDF.get(key, -1)
            if isTermInKey == -1:
                tempTF_IDF[key] = {}

            for k, v in value.iteritems():
                isDocInKey = tempTF_IDF[key].get(k, -1)
                if isDocInKey == -1:
                    tempTF_IDF[key][k] = {}
                tempTF_IDF[key][k] = v * idf[key]
        return tempTF_IDF

    def docHandler(self, invIndex, numDocs):
        print "Initializing Document Handler..."
        if numDocs == 0:
            self.numDocs = self.findNumDocs(invIndex)
        else:
            self.numDocs = numDocs
        return self.calcTF_IDF(invIndex)
