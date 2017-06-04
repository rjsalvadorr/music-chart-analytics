from datetime import datetime

import requests
from bs4 import BeautifulSoup

from . import constants
from .ultimateguitarstrategy import UltimateGuitarStrategy
from .databasehandler import DatabaseHandler
from .chartparser import ChartParser
from .objects.chartdata import ChartData

"""
Steps:

1. Get links for artist.
2. For each chord sheet, parse it for relevant data, and write the formatted chart out.
Potential filename format: artist-name_song-name_session-id.md
"""

class ChartScraper:
    def __init__(self):
        self.parser = ChartParser()
        self.dbHandler = DatabaseHandler()
        self.chordSheetLinks = []

        self.scrapeStrategies = []
        self.scrapeStrategies.append(UltimateGuitarStrategy())

        self.testModeEnabled = False
        self.scrapeCooldownEnabled = True


    def _isUrlValidTarget(self, url):
        """
        Returns true when the given URL hasn't been scraped before, or if it was scraped a while ago.
        For our purposes, 30 days is the cooldown time for a URL.
        """

        chartData = self.dbHandler.getChartByUrl(url)

        if chartData is None:
            return True

        dtScrape = datetime.strptime(chartData.updateTime, constants.DATETIME_FORMAT)
        dtNow = datetime.now()
        dtDifference = dtNow - dtScrape

        print("Days between the dates: " + str(dtDifference.days))

        if(dtDifference.days > constants.URL_SCRAPE_COOLDOWN_DAYS):
            return True
        else:
            return False


    def scrape(self, artistName):
        """
        Scrapes websites for song charts by a given artist, then feeds that information to the parser.
        After scraping is complete, the parser analysis is triggered.
        """
        scrapeSourceNames = []
        artistSourceUrls = []
        print("Scraping for " + artistName + " songs...")

        # Set up artist information, then send it to the parser.
        for scrapeStrategy in self.scrapeStrategies:
            scrapeSourceNames.append(scrapeStrategy.getSourceName())
            artistSourceUrls.append(scrapeStrategy.getArtistUrl(artistName))

        self.parser.setArtistData(artistName, scrapeSourceNames, artistSourceUrls)

        # Scrape the chart sources for song charts, then call the parser for each one.
        for scrapeStrategy in self.scrapeStrategies:
            songUrls = scrapeStrategy.getSongUrlsForArtist(artistName)

            for index, songUrl in enumerate(songUrls):
                if self.scrapeCooldownEnabled and not self._isUrlValidTarget(songUrl):
                    print("Invalid URL target: " + songUrl)
                    break

                if self.testModeEnabled and index >= constants.TEST_MODE_SONG_LIMIT:
                    break

                resp = requests.get(songUrl)
                pageContent = resp.content
                soup = BeautifulSoup(pageContent, "html.parser")
                chartContentHtml = soup.select(".js-tab-content")[0]
                chartContent = chartContentHtml.get_text()

                self.parser.parseChart(scrapeStrategy.getSongTitle(soup), songUrl, chartContent)

        print("Scraping complete!")
