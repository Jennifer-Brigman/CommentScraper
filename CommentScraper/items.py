import scrapy


class SiteItem(scrapy.Item):
    """
    The top level container class for site meta data.
    """
    url = scrapy.Field() # url of
    author_name = scrapy.Field()
    text = scrapy.Field()
    date_published = scrapy.Field()
    date_modified = scrapy.Field()
    headline = scrapy.Field()
    publisher_name = scrapy.Field()


class CommentItem(scrapy.Item):
    """
    The top level container class for comments.
    """
    time_stamp = scrapy.Field(serializer=str)
    author = scrapy.Field()
    author_id = scrapy.Field()
    id = scrapy.Field()
    in_reply_to = scrapy.Field()
    text = scrapy.Field()
    parent_article_url = scrapy.Field()


class GuardianSiteItem(SiteItem):
    """GuardianSiteItem contains all the information for a scrapers url.
     """

    author_profile = scrapy.Field()
    schema_org_type = scrapy.Field()
    sub_meta_titles = scrapy.Field()

    author_name_same_as = scrapy.Field()
    publisher_name_same_as = scrapy.Field()
    publisher_schema_org_type = scrapy.Field()

    keywords = scrapy.Field()
    description = scrapy.Field()
    image_descriptions = scrapy.Field()


class GuardianSiteCommentItem(CommentItem):
    """GuardianSiteItem contains all the information for a scrapers url.
     """
