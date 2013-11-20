from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

import re
import os
import json


class NflScheduleSpider(BaseSpider):
    name = "schedulespider"
    allowed_domains = ["nfl.com"]
    start_urls = [
        "http://www.nfl.com/schedule",
    ]

    GAMEBOOK_BASE_DIR = 'gamebooks'
    NFL_BASE_URL = 'http://www.nfl.com'

    GAMEBOOK_URL_PATTERN = r'/liveupdate/gamecenter/\d+/\w+\.pdf'
    WEEK_PATTERN = r'week\s+\:\s+\"(\d+)\",'
    SEASONTYPE_PATTERN = r'seasontype\s+\:\s+\"(\w+)\",'
    SEASON_PATTERN = r'year\s+\:\s+(\d{4}),'
    GAMEID_PATTERN = r'id\s+\:\s+\"(\d{10})\",'
    GAMEKEY_PATTERN = r'key\s+\:\s+\"(\d{5})\",'
    TEAMS_PATTERN = r'teams\s+\:\s+(\{.*\}),'

    def save_gamebook(self, response):
        """
        Process and save an NFL games gamebook PDF
        """

        gameid = response.meta.get('gameid', 0)
        gamekey = response.meta.get('gamekey', 0)
        team1 = response.meta.get('team1', 'UNKNOWN')
        team2 = response.meta.get('team2', 'UNKNOWN')
        season = response.meta.get('season', 0)
        seasontype = response.meta.get('seasontype', 'unknown')
        week = response.meta.get('week', 0)

        directory = os.path.join(
                self.GAMEBOOK_BASE_DIR,
                str(season),
                seasontype + str(week),
            )
        filename = '{}-{}_{}-{}.pdf'.format(gameid, gamekey, team1, team2)

        if not os.path.isdir(directory):
            os.makedirs(directory)

        # Replace the gamebook file
        with open(os.path.join(directory, filename), 'w') as fd:
            fd.write(response.body)

    def parse_gamecenter(self, response):
        """
        Parses and processes the an individual game's gamecenter page
        """

        metadata = self._game_metadata(response)

        for gamebook_url in set(re.findall(self.GAMEBOOK_URL_PATTERN, response.body)):
            url = self.NFL_BASE_URL + gamebook_url
            yield Request(url, callback=self.save_gamebook, meta=metadata)

    def parse(self, response):
        """
        Parses and processes the NFL schedule page
        """

        sel = Selector(response)

        # Parse game links and then call this method for each one
        games = sel.xpath('//div[@data-gamestate="POST"]')
        for game in games:
            url = game.xpath('@data-gc-url').extract()[0]
            yield Request(url, callback=self.parse_gamecenter)

    def _game_metadata(self, response):
        gameid_match = re.search(self.GAMEID_PATTERN, response.body)
        gameid = int(gameid_match.groups()[0]) if gameid_match is not None else 0

        gamekey_match = re.search(self.GAMEKEY_PATTERN, response.body)
        gamekey = int(gamekey_match.groups()[0]) if gamekey_match is not None else 0

        week_match = re.search(self.WEEK_PATTERN, response.body)
        week = int(week_match.groups()[0]) if week_match is not None else 0

        season_match = re.search(self.SEASON_PATTERN, response.body)
        season = int(season_match.groups()[0]) if season_match is not None else 0

        seasontype_match = re.search(self.SEASONTYPE_PATTERN, response.body)
        seasontype = seasontype_match.groups()[0] if seasontype_match is not None else 'unknown'

        teams_match = re.search(self.TEAMS_PATTERN, response.body)
        if teams_match:
            teams = json.loads(teams_match.groups()[0]).keys()
        else:
            teams = ['UNKNOWN', 'UNKNOWN']

        return {
            'gameid': gameid,
            'gamekey': gamekey,
            'week': week,
            'season': season,
            'seasontype': seasontype,
            'team1': teams[0],
            'team2': teams[1],
        }
