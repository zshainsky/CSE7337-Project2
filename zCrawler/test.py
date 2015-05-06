from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals

# from testspiders.spiders.followall import FollowAllSpider

from spiders.zackSpider import zackSpider
from scrapy.utils.project import get_project_settings

def setup_crawler():
    # spider = FollowAllSpider(domain=domain)
    spider = zackSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

    log.start()
    reactor.run()

setup_crawler()
# for domain in ['scrapinghub.com', 'insophia.com']:
#     setup_crawler(domain)
