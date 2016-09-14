# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from CommentScraper import items


class GuardianItemPipeline(object):
    """
    We can define business logic for how to control items generated during scraping
    """

    def __init__(self):

        # Save file in parent directory. Use os.pardir to indicate this as this is operator independent.
        self.file = open(os.path.join(os.pardir, "data/guardian_site_items"), "w")

        # Establish database connection using the settings in settings.py
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):

        # Write item to file in json format
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        # Output item to mongodb database
        if self.is_valid(item):
            if isinstance(item, items.GuardianSiteItem):
                collection_string = self.normalise_collection_name(item)
                collection = self.db[collection_string]  # create collection for this item if none exists
                collection_id = collection.insert(dict(item))  # insert item key/values into this collection
                self.collection_string = collection_string
                self.collection_id = collection_id
                logging.info("Writing" + str(item) + " to collection " + str(collection))
            elif isinstance(item, items.GuardianSiteCommentItem):
                # Get collection name for site.
                collection = self.db.get_collection(self.collection_string)
                collection.update({'_id': self.collection_id}, {'$push': {'comments': dict(item)}})
                logging.info("Writing" + str(item) + " to collection " + str(collection))
        else:
            raise DropItem("Missing {0}!".format(item))

        return item

    def normalise_collection_name(self, item):
        collection_string = "".join(filter(str.isalnum, item['headline'] + item['date_published'])).lower()
        collection_string = collection_string + '_' + type(item).__name__.lower()  # keep only alphanumeric
        return collection_string

    def is_valid(self, item):
        """
        :param item: item to validate
        :return: True if item passes validation tests.
        """
        return True

