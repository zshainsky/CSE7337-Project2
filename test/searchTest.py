from __future__ import division
from copy import deepcopy
import math

from InvertedIndex import InvertedIndex
from Query import Query
from tfidf import TFIDF

#Search Test
'''
invIndex = {'and': {0: 1, 2: 1}, 'limited': {0: 1, 2: 1}, 'project.': {0: 1, 1: 1, 2: 1}, 'saving': {1: 1, 2: 1}, 'text': {0: 1, 2: 6}}
#invIndex = {'and': {0: 1, 2: 1}, 'limited': {0: 1, 2: 1}, 'project.': {0: 1, 1: 1, 2: 1}, 'saving': {1: 1, 2: 1}, 'text': {0: 1, 2: 1}, 'is': {0: 1}, 'describe': {1: 1, 2: 1}, 'will': {0: 1, 2: 1}, 'in': {0: 1, 1: 1, 2: 2}, 'need': {1: 1, 2: 1}, 'query': {1: 1, 2: 1}, 'saved': {1: 1, 2: 1}, 'web': {0: 1, 2: 1}, 'use': {0: 1, 1: 1, 2: 1}, 'from': {1: 1, 2: 1}, 'built': {0: 1, 2: 1}, 'for': {0: 1, 1: 1, 2: 2}, 'files.': {0: 1, 2: 1}, 'support': {1: 2, 2: 2}, 'detail': {1: 1, 2: 1}, '1': {0: 1, 2: 1}, 'to': {1: 3, 2: 3}, 'html': {0: 1, 2: 1}, 'probably': {0: 1, 1: 1, 2: 1}, 'you': {0: 2, 1: 3, 2: 5}, 'that': {0: 1, 1: 1, 2: 2}, 'modify': {1: 1, 2: 1}, 'space,': {0: 1, 2: 1}, 'what': {1: 1, 2: 1}, 'how': {1: 1, 2: 1}, 'words': {1: 2, 2: 2}, 'pages': {1: 1, 2: 1}, 'a': {0: 1, 2: 1}, 'engine.': {1: 1, 2: 1}, 'this': {1: 2, 2: 2}, 'crawled': {0: 1, 2: 1}, 'ill': {1: 1}, 'changed': {1: 1, 2: 1}, 'project': {0: 1, 2: 1}, 'traversed': {1: 1, 2: 1}, 'of': {1: 1, 2: 1}, 'the': {0: 1, 1: 3, 2: 4}, 'looking': {0: 1, 2: 1}, 'crawler': {0: 1, 2: 1}}
cacheDocs = {0: ['copy.txt', 'use the web crawler you built in project 1 that crawled a limited space, looking for text and html files.'], 1: ['project.txt', 'use ill probably need to modify how you saved the words from the pages that you traversed to support this'], 2: ['project_instructions.txt', 'use the web crawler you built in project 1 that crawled a limited space, looking for text and html files.']}
query = "and limited saving"
'''

#Test Data from class
doc1 = "This is box one"
doc2 = "This is box one This is box one"
doc3 = "This is one collection of stuff in a box"
invIndex = {'This': {1: 1, 2: 2, 3: 1}, 'is': {1: 1, 2: 2, 3: 1}, 'box': {1: 1, 2: 2, 3: 1}, 'one': {1: 1, 2: 2, 3: 1}, 'collection': {3: 1}, 'of': {3: 1}, 'stuff': {3: 1}, 'in': {3: 1}, 'a': {3: 1}}
query = "box one"

##################### Question 3 Function ######################
def createTermFrequencyMatrix(invIndex):
    tempDocMatrix = {}
    for key, value in invIndex.iteritems():
        for k, v in value.iteritems():
            isDocInMatrix = tempDocMatrix.get(k, -1)
            if isDocInMatrix == -1:
               tempDocMatrix[k] = {key: v}
            else:
                tempDocMatrix[k].update({key: v})
        print tempDocMatrix
    print "Final:", tempDocMatrix
    return tempDocMatrix

'''
###################### Document Functions ######################
def findNumDocs(invIndex):
    numDocs = 0
    for key, value in invIndex.iteritems():
        for k, v in value.iteritems():
            if k > numDocs:
                numDocs = k
    return numDocs

def calcDocFrequency(invIndex):
    df = {}
    for key, val in invIndex.iteritems():
        df[key] = len(val)
    return df

def sumTermFrequency(invIndex):
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

def normalizeTermFrequency(invIndex):
    tfSum = sumTermFrequency(invIndex)

    #Might need...Thought shallow copy would alter both copies of the data if one was edited
    normalizedIndex = deepcopy(invIndex)
    #normalizedIndex = dict.copy(invIndex)

    for key, value in normalizedIndex.iteritems():
        for k, v in value.iteritems():
            normalizedIndex[key][k] = v/tfSum[k]
    #return new inverted index with normalized term frequency values
    return normalizedIndex

def calcIDF(invIndex):
    numDocs = findNumDocs(invIndex)
    df = calcDocFrequency(invIndex)
    idf = {}

    for key, value in df.iteritems():
        idf[key] = 1 + math.log10(numDocs/df[key])
    return idf


def calcTF_IDF(invIndex):
    normTF = normalizeTermFrequency(invIndex)
    idf = calcIDF(invIndex)

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

def docHandler(invIndex):
    print "Initializing Document Handler..."
    return calcTF_IDF(invIndex)
'''
'''
###################### Query Functions ######################
def normQueryTF(frequencyDict, numTerms):
    for key, val in frequencyDict.iteritems():
        frequencyDict[key] = val/numTerms
    return frequencyDict

def calcQueryCollectionFrequency(queryWords, numTerms):
    collectionFrequency = 0
    frequencyDict = {}
    for i, word in enumerate(queryWords):
        for j, checkWord in enumerate(queryWords):
            if word == checkWord:
                collectionFrequency += 1
        frequencyDict[word] = collectionFrequency
        collectionFrequency = 0
    return frequencyDict

def calcQueryIDF(freqDict, numDocs):
    tempIDF = {}
    for key, value in freqDict.iteritems():
        #df is 1 because only one document (query) for terms to be in
        tempIDF[key] = 1 + math.log10(numDocs/1)
    return tempIDF

def calcQueryTF_IDF(normFrequencyDict, queryIDF):
    tf_idf = {}
    for key, value in normFrequencyDict.iteritems():
        tf_idf[key] = normFrequencyDict[key] * queryIDF[key]
    return tf_idf

def queryHandler(query, invIndex):
    print "Initializing Query Handler..."
    temp = query.split(' ')
    #Remove stop words, clean case/punct, stemm

    numTerms = len(temp)
    numDocs = findNumDocs(invIndex)

    freqDict = calcQueryCollectionFrequency(temp, numTerms)
    normFrequencyDict = normQueryTF(freqDict, numTerms)

    #I believe this is always 1 for a query because df is number of docs in collection with term and query is one doc and the only doc in the collection
    #calcQueryDF(temp)
    queryIDF = calcQueryIDF(freqDict, numDocs)
    queryTF_IDF = calcQueryTF_IDF(normFrequencyDict, queryIDF)

    return queryTF_IDF

###################### Cosine Similarity Functions ######################
def calcQueryDocDotProduct(docTF_IDF, queryTF_IDF):
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

def calcQueryEuclideanLength(queryTF_IDF):
    tempLength = 0
    for key, value in queryTF_IDF.iteritems():
        tempLength += value * value
    return math.sqrt(tempLength)

def calcDocEuclideanLength(docTF_IDF, queryTF_IDF):
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



def calcCosSimilarity(queryDocDotProducts, docLength, queryLength):
    tempCosSimDocs = {}
    tempCosSimVal = 0

    for key, value in queryDocDotProducts.iteritems():
        tempCosSimDocs[key] = (queryDocDotProducts[key])/(docLength[key]*queryLength)
    return tempCosSimDocs

def cosSimilarityHandler(docTF_IDF, queryTF_IDF):
    print "Initializing Cosine Similarity Handler..."
    queryDocDotProducts = calcQueryDocDotProduct(docTF_IDF, queryTF_IDF)
    docLength = calcDocEuclideanLength(docTF_IDF, queryTF_IDF)
    queryLength = calcQueryEuclideanLength(queryTF_IDF)

    return calcCosSimilarity(queryDocDotProducts, docLength, queryLength)
'''

def parseQuery(query, invIndex):
    #Both handlers return the respective TF_IDFs
    #docTF_IDF can be run once after crawl
    tempTFIDF = TFIDF()
    queryObj = Query(query)

    docTF_IDF = tempTFIDF.docHandler(invIndex, 0)
    queryTF_IDF = queryObj.queryHandler(queryObj.query, invIndex)
    cosSimByDoc = queryObj.cosSimilarityHandler(docTF_IDF, queryTF_IDF)
    print cosSimByDoc
    print "Cosine Similarity by document:", cosSimByDoc
    return cosSimByDoc

def printDictionaries(d):
    print "{:<8} {:<10}".format('DocID ,','Number')
    for k, v in d.iteritems():
        num = v
        print "{:<8}{:<10}".format(k, num)

#temp = createTermFrequencyMatrix(invIndex)
#printDictionaries(temp)
#cosineSimilarityByDocument = parseQuery(query, invIndex)



def main():
    #All Crawling here!
    #InvIndex()


    #Infinate loop
    while(1):
        query = raw_input("Please enter a query: ")
        print "Your query is:", query

        parseQuery(query, invIndex)
        print


if __name__ == "__main__":
    main()

