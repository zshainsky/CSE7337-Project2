


from CrawlerWorker import CrawlerWorker 
from multiprocessing.queues import Queue
import os
import spiders
from spiders.zackSpider import zackSpider



print "in main"
result_queue = Queue()
# cwd = os.getcwd()
# os.chdir(cwd + "/spiders")
crawler = CrawlerWorker(zackSpider(), result_queue)
crawler.start()
for item in result_queue.get():
    print item
    # yield item

