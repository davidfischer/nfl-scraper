from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from .nfl_spider import NflScheduleSpider

import re


class NflHistoricalSpider(NflScheduleSpider):
    name = "historicalspider"
    allowed_domains = ["nfl.com"]
    start_urls = []

    GAMEBOOK_BASE_DIR = 'gamebooks'
    NFL_BASE_URL = 'http://www.nfl.com'

    def __init__(self, year=None, week=None, *args, **kwargs):
        super(NflHistoricalSpider, self).__init__(*args, **kwargs)
        if year is None:
            self.log('No year specified!')
        else:
            self.year = year
            self.week = week
            self.url_pattern = r'^/scores/{}/\w+$'.format(year)
            self.start_urls = ['http://www.nfl.com/scores/{}/REG1'.format(year)]

    def parse_week(self, response):
        sel = Selector(response)

        for link in sel.xpath('//a[@class="game-center-link"]'):
            url = self.NFL_BASE_URL + link.xpath('@href').extract()[0]
            yield Request(url, callback=self.parse_gamecenter)


    def parse(self, response):
        """
        Parses and processes the NFL scores page which links to all previous
        games from all weeks of the given year
        """

        sel = Selector(response)

        for link in sel.xpath('//a[@href]'):
            href = link.xpath('@href').extract()[0]
            if re.search(self.url_pattern, href) is not None:
                url = self.NFL_BASE_URL + href
                if self.week is None or 'REG{}'.format(self.week) in url:
                    yield Request(url, callback=self.parse_week)
