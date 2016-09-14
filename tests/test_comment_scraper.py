from unittest import TestCase
from CommentScraper.spiders import guardian_spider


class TestScraperUtils(TestCase):
    """
    Tests the key comment scraper
    """
    source = 'https://www.theguardian.com/environment/' + \
             'climate-consensus-97-per-cent/2016/aug/22/' + \
             'historical-documents-reveal-arctic-sea-ice-is-disappearing-at-record-speed'

    def setUp(self): pass

    def tearDown(self): pass

    def test_get_html(self):
        """
        Succeed if beautifulsoup4 can fetch the default test url
        """
        article_soup = guardian_spider.get_html(self.source)
        if article_soup:
            pass
        else:
            self.fail("Couldn't get html.")

    def test_num_pagination_buttons(self):
        """
        Succeed if the number of comments for the test url is above a last confirmed number of comment pages.
        """
        article_soup = guardian_spider.get_html(self.source)
        comment_url = article_soup.find(class_='discussion__heading').find('a')['href']
        comment_soup = guardian_spider.get_html(comment_url)
        total_pages = guardian_spider.num_pagination_buttons(comment_soup)

        if total_pages > 10:  # There were at least 18 last time we checked. There should at least be 10 or more.
            pass
        else:
            self.fail("We know that in this example there is more than one page of comments.")

    def test_scrape_comments(self):
        output = guardian_spider.scrape_comments(self.source)
        if output:
            pass
        else:
            self.fail("Nothing scraped.")

    def test_save_comments(self):
        self.fail()
