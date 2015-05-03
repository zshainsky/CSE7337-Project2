# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PageItem(scrapy.Item):
	#Generated ID for this specific URL
    doc_id = scrapy.Field()
    #url of the page being crawled
    url = scrapy.Field()
    #list of words on the page
    words = scrapy.Field()

