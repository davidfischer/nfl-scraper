NFL Gamebook Scraper
====================

This is a utility for saving NFL gamebooks, the PDFs the NFL makes available
to assist in media coverage of NFL football games.


Prerequisites
-------------

* Python 2.7 (exactly)
* [Scrapy][scrapy-link]


Usage
-----

Download the most recent week's gamebooks:

    % scrapy crawl schedulespider

Download the data from a specific historical year (2001+):

    % scrapy crawl historicalspider -a year=2011

Download the data from a specific historical year and week:

    % scrapy crawl historicalspider -a year=2011 -a week=18 -a weektype=POST
    % scrapy crawl historicalspider -a year=2011 -a week=1 -a weektype=PRE
    % scrapy crawl historicalspider -a year=2011 -a week=11  # REG


[scrapy-link]: http://scrapy.org/
