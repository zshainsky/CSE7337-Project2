__author__ = 'zshainsky'
from InvertedIndex import InvertedIndex
from Query import Query


def main():
    #All Crawling here!
    invIndex = InvertedIndex()
    #invIndex.callScraper()
    invIndex.inverted_index = {'This': {1: 1, 2: 2, 3: 1}, 'is': {1: 1, 2: 2, 3: 1}, 'box': {1: 1, 2: 2, 3: 1}, 'one': {1: 1, 2: 2, 3: 1}, 'collection': {3: 1}, 'of': {3: 1}, 'stuff': {3: 1}, 'in': {3: 1}, 'a': {3: 1}}

    queryObj = Query()


    #Infinate loop
    while(1):
        queryObj.query = raw_input("Please enter a query: ")
        print "Your query is:", queryObj.query

        queryObj.parseQuery(queryObj.query, invIndex.inverted_index)
        print


if __name__ == "__main__":
    main()