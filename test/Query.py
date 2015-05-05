from __future__ import division
from copy import deepcopy
import math

from InvertedIndex import InvertedIndex
from Parser import Parser
from tfidf import TFIDF




class Query:

    def __init__(self, queryString=""):
        print "Constructing Query Object!"
        self.invIndex = InvertedIndex()
        self.tfidf = TFIDF()
        self.query = queryString

    ###################### Other Functions ######################
    def removeMissingQueryTerms(self, queryList, invIndex):
        removedWords = []
        for word in queryList:
            isWordInIndex = invIndex.get(word, -1)
            if isWordInIndex == -1:
                removedWords.append(word)
                queryList.remove(word)
        return removedWords

    ###################### Query Functions ######################
    def normQueryTF(self, frequencyDict, numTerms):
        print numTerms, frequencyDict
        for key, val in frequencyDict.iteritems():
            frequencyDict[key] = val/numTerms
        return frequencyDict

    def calcQueryCollectionFrequency(self, queryWords):
        collectionFrequency = 0
        frequencyDict = {}
        for i, word in enumerate(queryWords):
            for j, checkWord in enumerate(queryWords):
                if word == checkWord:
                    collectionFrequency += 1
            frequencyDict[word] = collectionFrequency
            collectionFrequency = 0
        return frequencyDict

    def calcQueryIDF(self, freqDict, numDocs):
        tempIDF = {}
        for key, value in freqDict.iteritems():
            #df is 1 because only one document (query) for terms to be in
            tempIDF[key] = 1 + math.log10(numDocs/1)
        return tempIDF

    def calcQueryTF_IDF(self, normFrequencyDict, queryIDF):
        tf_idf = {}
        for key, value in normFrequencyDict.iteritems():
            tf_idf[key] = normFrequencyDict[key] * queryIDF[key]
        return tf_idf

    def queryHandler(self, query, invIndex):
        print "Initializing Query Handler..."
        queryWordList = query.split(' ')

        #Remove stop words, clean case/punct, stemm
        print "Parsing Query Words..."
        parser = Parser()
        print parser.fullParse(queryWordList)
        print "Parsed Query Words..."

        removedWords = self.removeMissingQueryTerms(queryWordList, invIndex)
        if len(queryWordList) == 0:
            return -1
        print "These words were not found and removed from the query: ", removedWords
        print "Updated Query Words List", queryWordList


        numTerms = len(queryWordList)
        numDocs = self.tfidf.findNumDocs(invIndex)

        freqDict = self.calcQueryCollectionFrequency(queryWordList)
        normFrequencyDict = self.normQueryTF(freqDict, numTerms)

        #I believe this is always 1 for a query because df is number of docs in collection with term and query is one doc and the only doc in the collection
        #calcQueryDF(temp)
        queryIDF = self.calcQueryIDF(freqDict, numDocs)
        queryTF_IDF = self.calcQueryTF_IDF(normFrequencyDict, queryIDF)

        return queryTF_IDF

    ###################### Cosine Similarity Functions ######################
    def calcQueryDocDotProduct(self, docTF_IDF, queryTF_IDF):
        docDotProducts = {}
        dotProd = 0

        for key, value in queryTF_IDF.iteritems():
            isKeyInDoc = docTF_IDF.get(key, -1)
            if isKeyInDoc != -1:
                for k, v in docTF_IDF[key].iteritems():
                    isDocIdInTempDotProd = docDotProducts.get(k, -1)
                    if isDocIdInTempDotProd == -1:
                        docDotProducts[k] = value * v
                    else:
                        docDotProducts[k] += value * v
            else:
                print key, "not found in index"

        return docDotProducts

    def calcQueryEuclideanLength(self, queryTF_IDF):
        tempLength = 0
        for key, value in queryTF_IDF.iteritems():
            tempLength += value * value
        return math.sqrt(tempLength)

    def calcDocEuclideanLength(self, docTF_IDF, queryTF_IDF):
        tempLength = 0
        tempDocEuclideanLength = {}

        for key, value in queryTF_IDF.iteritems():
            for k, v in docTF_IDF[key].iteritems():
                isDocInDict = tempDocEuclideanLength.get(k, -1)
                if isDocInDict == -1:
                    tempDocEuclideanLength[k] = v*v
                else:
                    tempDocEuclideanLength[k] += v*v

        for newKey, newVal in tempDocEuclideanLength.iteritems():
            tempDocEuclideanLength[newKey] = math.sqrt(tempDocEuclideanLength[newKey])
        return tempDocEuclideanLength



    def calcCosSimilarity(self, queryDocDotProducts, docLength, queryLength):
        tempCosSimDocs = {}
        tempCosSimVal = 0

        for key, value in queryDocDotProducts.iteritems():
            tempCosSimDocs[key] = (queryDocDotProducts[key])/(docLength[key]*queryLength)
        return tempCosSimDocs

    def cosSimilarityHandler(self, docTF_IDF, queryTF_IDF):
        print "Initializing Cosine Similarity Handler..."
        queryDocDotProducts = self.calcQueryDocDotProduct(docTF_IDF, queryTF_IDF)
        docLength = self.calcDocEuclideanLength(docTF_IDF, queryTF_IDF)
        queryLength = self.calcQueryEuclideanLength(queryTF_IDF)

        return self.calcCosSimilarity(queryDocDotProducts, docLength, queryLength)

    def parseQuery(self, query, invIndex):
        #Both handlers return the respective TF_IDFs
        #docTF_IDF can be run once after crawl
        tfidf = TFIDF()
        docTF_IDF = tfidf.docHandler(invIndex, 0)

        queryTF_IDF = self.queryHandler(query, invIndex)
        if queryTF_IDF == -1:
            print "No words from your search were found in any documents...Please try new search terms!"
            return -1

        cosSimByDoc = self.cosSimilarityHandler(docTF_IDF, queryTF_IDF)
        print "Cosine Similarity by document:", cosSimByDoc
        return cosSimByDoc



    def printDictionaries(self, d):
        print "{:<8} {:<10}".format('DocID ,','Number')
        for k, v in d.iteritems():
            num = v
            print "{:<8}{:<10}".format(k, num)

    #temp = createTermFrequencyMatrix(invIndex)
    #printDictionaries(temp)
    #cosineSimilarityByDocument = parseQuery(query, invIndex)
