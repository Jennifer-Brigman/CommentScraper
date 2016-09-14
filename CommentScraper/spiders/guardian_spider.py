import urllib.request
import urllib.robotparser

import scrapy
from bs4 import BeautifulSoup
from extruct.w3cmicrodata import MicrodataExtractor
from CommentScraper import items

class GuardianSpider(scrapy.Spider):

    # define spider specific settings
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = ['https://www.theguardian.com/environment/' +\
                  'climate-consensus-97-per-cent/2016/aug/22/' +\
                  'historical-documents-reveal-arctic-sea-ice-is-disappearing-at-record-speed'
                  ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES':  # define the pipelines for handling items
            {'CommentScraper.pipelines.GuardianItemPipeline': 1}
    }

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        if response.url in self.start_urls:
            yield self.parse_article(response)

        for url in get_comment_pages_urls(response):
            request = scrapy.Request(url, callback=self.parse_item)
            request.meta['parent_article_url'] = response.url
            yield request

    def parse_article(self, response):

        print('Fetching {0}'.format(response.url))

        extractor = MicrodataExtractor()
        meta_items = extractor.extract(response.body_as_unicode(), response.url)['items']
        item = items.GuardianSiteItem()
        meta_item = meta_items[1]

        properties = meta_item['properties']
        if properties.get('author', {}):
            name_properties = properties['author']['properties']
            item['author_name'] = name_properties['name']
            item['author_name_same_as'] = name_properties['sameAs']
            item['schema_org_type'] = properties['author']['type']

        if properties.get('publisher', {}):
            publisher_properties = properties['publisher']['properties']
            item['publisher_name'] = publisher_properties['name']
            item['publisher_name_same_as'] = publisher_properties['sameAs']
            item['publisher_schema_org_type'] = properties['publisher']['type']

        item['url'] = response.url
        item['headline'] = properties['headline']
        item['description'] = properties['description']
        item['date_published'] = properties['datePublished']
        item['date_modified'] = properties['dateModified']
        item['keywords'] = properties['keywords']
        item['text'] = properties['articleBody']

        if properties.get('image', {}):
            image_descriptions = []
            for image_dict in properties['image']:
                image_descriptions.append(image_dict['properties']['description'])

            item['image_descriptions'] = image_descriptions

        return item

    def parse_item(self, response):
        """
        Parses comments from the comment section.
        :param article_url: the parent url where the article body is contained
        :param response: The response object for the web page in question.
        :return: Yields a comment item populated from response url.

        """
        print('Fetching {0}'.format(response.url))
        soup = BeautifulSoup(response.body, "html.parser")

        for comment in soup.select('li.d-comment'):

            comment_item = items.GuardianSiteCommentItem()

            comment_item['parent_article_url'] = response.meta['parent_article_url']
            comment_item['id'] = comment['data-comment-id']
            comment_item['time_stamp'] = comment['data-comment-timestamp']
            comment_item['author'] = comment['data-comment-author']
            comment_item['author_id'] = comment['data-comment-author-id']

            body = comment.find(class_='d-comment__body')
            if body.blockquote is not None:
                body.blockquote.clear()
            comment_item['text'] = body.getText().strip()

            reply_to = comment.find(class_='d-comment__reply-to-author')
            if reply_to is not None:
                link = reply_to.parent['href'].replace('#comment-', '')
                comment_item['in_reply_to'] = link
            else:
                comment_item['in_reply_to'] = ''
                # TODO Perhaps items allow default values?

            yield comment_item

def get_comment_pages_urls(response):
    """
    Given a URL, this function finds the comments section and cycles through the pages using a helper
    function to gather the comments from each page.
    :param response:
    :return: All comments

    """
    # get the web page
    article_soup = BeautifulSoup(response.body, "html.parser")

    # load the comment section from this web page
    comment_url = article_soup.find(class_='discussion__heading').find('a')['href']
    print('Finding comments for ({0})\n'.format(response.url))

    comment_soup = get_html(comment_url)

    # cycle through the pages in the comment section and aggregate comments
    total_pages = num_pagination_buttons(comment_soup)

    for i in range(total_pages, 0, -1):
        params = urllib.parse.urlencode({'page': i})
        url = '{0}?={1}'.format(comment_url, params)

        yield url


def num_pagination_buttons(comment_soup):
    """
    :type comment_soup: beautifulsoup parse
    :param comment_soup:
    :return: number of pages of the comment section

    :Example:

    num_pagination_buttons(comment_soup) = 10
    indicates there are 10 discussion pages for comment_soup

    """

    # Get the page number buttons.
    pagination_btns = comment_soup.find_all('a', class_='pagination__action')
    last_pagination_btn = comment_soup.find('a', class_='pagination__action--last')

    # If there are page number buttons then get the
    if last_pagination_btn is not None:

        # there is more than 1 pagination button
        total_pages = int(last_pagination_btn['data-page'])
    elif pagination_btns:

        # there is 1 pagination button
        total_pages = int(pagination_btns[-1]['data-page'])
    else:

        # there are no pagination buttons
        total_pages = 1

    return total_pages


def get_html(url):
    """
    :type url: string
    :param url
    :return: beautiful soup html for the url
    :rtype: beautifulsoup html
    """

    with urllib.request.urlopen(url) as urlSession:
        html = urlSession.read()
    return BeautifulSoup(html, "html.parser")
