#-*- coding: utf8
from __future__ import unicode_literals
import urllib
from ir_webstats.client import iRWebStats


class ClubStats(object):


    def __init__(self):
        self._irw = iRWebStats()


    def login(self, username, password):
        self._irw.login(username, password)


    def fetch_season_standings(self, series_name, club_name):
        season = self.get_current_season_data(series_name)
        club_id = self.get_club_id(club_name)
        standings, _ = self._irw.season_standings(season["seasonid"], season["carclasses"][0], club=club_id)
        return standings



    def get_club_id(self, clubname):
        irw = self._irw
        for club_id in irw.CLUBS:
            if irw.CLUBS[club_id]["shortclubname"] == clubname:
                return irw.CLUBS[club_id]["id"]
        else:
            raise LookupError("Club ID not found for {}".format(clubname))


    def get_current_season_data(self, series_name):
        irw = self._irw
        for season in irw.SEASON:
            if season["seriesname"].strip() == series_name:
                return season
        else:
            raise LookupError("Series '{}' not found".format(series_name))


def unquote_string(text):
    unqouted = urllib.parse.unquote(text)
    unqouted = unqouted.replace("+", " ")
    return unqouted