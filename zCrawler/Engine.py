__author__ = 'zshainsky'
from InvertedIndex import InvertedIndex
from Query import Query
import os
from collections import OrderedDict
from operator import itemgetter

def main():
    #All Crawling here!
    crawlSpider();
    invIndex = InvertedIndex()
    invIndex.loadPickles()

    queryObj = Query()

    os.system("clear")

    #Infinite loop
    while(1):

        print""
        print""
        print""

        invIndex.createTermFrequencyMatrix()
        queryObj.query = raw_input("Please enter a query for zackSpider: ")
        print "Your query is:", queryObj.query

        returnDocs = queryObj.parseQuery(queryObj.query, invIndex.inverted_index)
        if (returnDocs > 0):
            returnedDocs = sorted(returnDocs.items(),key=itemgetter(1), reverse=True)
            os.system("clear")            
            print""
            print""
            print""
            print "The following documents are ranked from highest to lowest similarity for your query: "
            print"---------------------------------------------------------------------------------------" 

            print "{:<5} {:<15} {:<55} {:<10}".format('Doc', 'Similarity', 'Url','Preview')
            for key in returnedDocs:

                docKey = key[0]-1
                doc = invIndex.collections_index[docKey]
                sim = key[1]
                print "{:<5} {:<15.10f} {:<55} {:<10}".format(docKey, sim, doc[0], doc[1])

            print""
            print""

        else:
            print "No results."
            print""
            print""



def crawlSpider():
    activeDirectory = os.getcwd();
    os.chdir("../zCrawler")
    os.system("scrapy crawl zackSpider")
    os.chdir(activeDirectory)


if __name__ == "__main__":
    main()