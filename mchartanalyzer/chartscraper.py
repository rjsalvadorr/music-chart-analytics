import requests
from bs4 import BeautifulSoup

from .ultimateguitarstrategy import UltimateGuitarStrategy
from .chartparser import ChartParser
from .chartdata import ChartData

"""
Steps:

1. Get links for artist.
2. For each chord sheet, parse it for relevant data, and write the formatted chart out.
Potential filename format: artist-name_song-name_session-id.md
"""

class Scraper:
    def __init__(self):
        self.parser = MusicChartParser()
        self.chordSheetLinks = []

        self.scrapeStrategies = []
        self.scrapeStrategies.append(UltimateGuitarStrategy())


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
            songUrls = scrapeStrategy.getSongUrls(artistName)

            for songUrl in songUrls:
                resp = requests.get(songUrl)
                pageContent = resp.content
                soup = BeautifulSoup(pageContent, "html.parser")
                chartContentHtml = soup.select(".js-tab-content")[0]
                chartContent = chartContentHtml.get_text()

                self.parser.parseChart(scrapeStrategy.getSongTitle(soup), songUrl, chartContent)

        print("Scraping complete!")
