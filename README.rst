Introduction
===================

Welcome to the Comment Scraper project. The aim of the project is to provide web scraping for supported news websites. Given a set of topics such as 'climate change' and 'the environment', the web scraper will find related articles from supported news websites and scrape both the content of articles and comments about these articles and output these articles in various formats.

To run the project please be sure to check the 'Requirements.txt' file for project dependencies.

The full documentation for this project can be found at ReadTheDocs_.

.. _ReadTheDocs: http://commentscraper.readthedocs.io/en/latest/index.html

Output
================

**JSON**

The output of scraping will be stored in json format in directory 'data\'. If this directory does not already exist, it will be created in the root directory.

**Mongodb**

After installing mongodb you can run it by first opening a terminal and typing in 'mongod' to start the mongodb server process followed by command 'mongo in a new terminal to connect to this process. The settings used to configure the mongodb database are shown in settings.py.