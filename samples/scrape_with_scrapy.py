from scrapy.crawler import CrawlerProcess

from CommentScraper.spiders import guardian_spider

default_source = 'https://www.theguardian.com/environment/' + \
                 'climate-consensus-97-per-cent/2016/aug/22/' + \
                 'historical-documents-reveal-arctic-sea-ice-is-disappearing-at-record-speed'

spider = guardian_spider.GuardianSpider(domain=default_source)

process = CrawlerProcess()  # run the settings.py script

process.crawl(guardian_spider.GuardianSpider)
process.start()  # the script will block here until the crawling is finished
