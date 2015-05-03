

import scrapy
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from zCrawler.items import PageItem
import re
import urlparse
import time
import lxml
from lxml.html.clean import clean_html, Cleaner
import tfidf
import os
import io, json
import operator


SLEEP_TIME = 1
RESULTS_DIRECTORY = "CrawlerResults"

class zackSpider(scrapy.Spider):
    #Scrapy Specific Variables
    name = "zackSpider"
    allowed_domains = ["lyle.smu.edu"]
    start_urls = ["http://lyle.smu.edu/~fmoore/"]
    handle_httpstatus_list = [404]
    table = tfidf.tfidf()

    def __init__(self):
        self.doc_id = 0
        self.cur_link = ""
        self.unique_outgoing_links = []
        self.unique_test_data_pages = []
        self.unique_broken_links = []
        self.unique_images = []
        self.document_links = []
        self.PageItems = []
        self.visited = []
        self.pdf = re.compile('\.pdf')
        self.ppt = re.compile('\.ppt')
        self.pptx = re.compile('\.pptx')

        self.all_links = []
        self.broken_links = []
        self.image_links = []
        self.cur_fmoore_links = []
        self.cur_outgoing_links = []

    def print_links(self, links):
        for link in links:
            print link


    def parse(self, response):

        #self.doc_id = self.doc_id + 1
        self.cur_link = response.url

        # HANDLE IMAGES
        jpg_links = response.xpath('//img/@src').extract()
        for image in jpg_links:
            self.addToImageList(image)

        # ALL OTHER URL LINKS
        links = response.xpath('//a/@href').extract()

        # CHECK LINKS FOR ERROR/BROKEN LINKS 
        broken = False
        if response.status == 200: 
            self.doc_id = self.doc_id + 1
            selector = Selector(response)
            bodyText = ''.join(response.xpath("//body//text()").extract()).strip().split()
            self.parse_page(self.doc_id, self.cur_link, bodyText)
            self.addToVisitedList(self.cur_link)
            for relative_url in links:
                # IF THESE ARE DOCUMENTS, MARK THEM AS VISITED B/C WE WILL NOT SCRAPE THEM, BUT WE WANT TO TRACK THE LINK, AND THEY WILL CAUSE ERRORS BELOW
                if (re.search(self.pdf, relative_url) or re.search(self.ppt, relative_url) or re.search(self.pptx, relative_url) ):
                    if re.match(r'^http(s?)://lyle\.smu\.edu\/\~fmoore', relative_url):
                        self.addToDocsList(relative_url)
                    else:
                        absolute_link = urlparse.urljoin(self.start_urls[0], relative_url)
                        self.addToDocsList(absolute_link)

                else:
                    base_url = get_base_url(response)
                    absolute_link = urlparse.urljoin(base_url, relative_url)

                    self.all_links.append(absolute_link)

                    # IF IN OUR FMOORE DIRECTORY - VISIT AND SCRAPE - IF IT HAS NOT BEEN VISITED BEFORE
                    if re.match(r'^http(s?)://lyle\.smu\.edu\/\~fmoore', absolute_link):
                        if not self.didVisit(absolute_link):
                            self.cur_fmoore_links.append(absolute_link)
                            self.addToTestDataPagesList(absolute_link)
                            yield Request(absolute_link)
                        else:
                            pass
                    # OTHERWISE ADD TO THE OUTGOING LINKS AND DO NOT VISIT
                    else:
                        self.cur_outgoing_links.append(absolute_link)
                        self.addToOutgoingList(absolute_link)

        else:
            self.broken_links.append(self.cur_link)
            broken = True

        # create directory to hold crawler results
        if not os.path.exists("CrawlerResults"):
            os.makedirs("CrawlerResults")

        self.output_CrawlerResults("TestDataPages", self.unique_test_data_pages)
        self.output_CrawlerResults("OutgoingLinks", self.unique_outgoing_links)
        self.output_CrawlerResults("BrokenOrBadLinks", self.broken_links)
        self.output_CrawlerResults("LinksToDocuments", self.document_links)
        self.output_CrawlerResults("UniqueImageLinks", self.unique_images)
        self.output_CrawlerResults("TotalImageLinks", self.image_links)
        self.table.outputCorpusTable()
        self.table.outputTop20Words()
        self.table.graphTop20()

        self.all_links = []
        self.cur_fmoore_links = []
        self.cur_outgoing_links = []

    
    def parse_page(self, doc_id, url, bodyText):
        item = PageItem()
        item['url'] = url
        item['doc_id'] = doc_id
        #tempwords = self.remove_tags(bodyText)
        if len(bodyText) > 0:
            self.table.addDocument(doc_id, bodyText)
        self.table.generateCorpusTable()
        self.table.printCorpusTable()
        self.PageItems.append(item)


    def all_links(self, response):
        print "all_links():"

    def addToTestDataPagesList(self, fmoore_url):
        if fmoore_url not in self.unique_test_data_pages:
            self.unique_test_data_pages.append(fmoore_url)

    def addToOutgoingList(self, outgoing_url):
        if outgoing_url not in self.unique_outgoing_links:
            self.unique_outgoing_links.append(outgoing_url)

    def addToBrokenLinkList(self, broken_link):
        if broken_link not in self.unique_broken_links:
            self.unique_broken_links.append(broken_link)

    def addToImageList(self, image_url):
        # TAKE ALL IMAGES -- EVEN DUPES SO WE CAN COUNT
        self.image_links.append(image_url)
        if image_url not in self.unique_images:
            self.unique_images.append(image_url)

    def addToDocsList(self, doc_url):
        if doc_url not in self.document_links:
            self.document_links.append(doc_url)
            self.addToVisitedList(doc_url)

    def addToVisitedList(self, current_url):
        if current_url not in self.visited:
            self.visited.append(current_url)

    def didVisit(self, current_url):
        if current_url in self.visited:
            return True
        else:
            return False

    def output_CrawlerResults(self, filename, dataset):
        with io.open(RESULTS_DIRECTORY + '/' + filename + '.txt', 'w', encoding='utf-8') as f:
            for item in dataset:
                f.write(unicode("%s\n" % item))

    def outputCorpusTable(self):
        temp = sorted(self.table.corpus_dict(), key=operator.itemgetter(1), reverse=True)
        with io.open(RESULTS_DIRECTORY + '/Corpus.txt', 'w', encoding='utf-8') as f:
            for word in temp:
                f.write(unicode("{1}\n", temp[w]))

    def outputTop20Words(self):
        with io.open(RESULTS_DIRECTORY + '/Top20Words.txt', 'w', encoding='utf-8') as f:
            for item in self.table.top20_w:
                f.write(unicode("%s\n" % item))

    



