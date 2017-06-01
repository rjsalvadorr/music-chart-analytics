import requests
from bs4 import BeautifulSoup

from .logger import Logger
from .ultimateguitarstrategy import UltimateGuitarStrategy
from .musicchartparser.musicchartparser import MusicChartParser
from .musicchartparser.chartdata import ChartData

"""
Steps:

1. Get links for artist.
2. For each chord sheet, parse it for relevant data, and write the formatted chart out.
Potential filename format: artist-name_song-name_session-id.md
"""

class MusicChartScraper:
    def __init__(self):
        self.logger = Logger()
        self.parser = MusicChartParser()
        self.chordSheetLinks = []

        self.scrapeStrategies = []
        self.scrapeStrategies.append(UltimateGuitarStrategy())

    def log(self, text):
        self.logger.log(text)

    def scrape(self, artistName):
        """
        Scrapes websites for songs by a given artist.
        """
        print("Scraping for " + artistName + " songs...")
        for scrapeStrategy in self.scrapeStrategies:
            songUrls = scrapeStrategy.getSongUrls(artistName)
            self.log("\nURLs for " + artistName + " on " + scrapeStrategy.siteDomain + ":")

            for songUrl in songUrls:
                resp = requests.get(songUrl)
                pageContent = resp.content
                soup = BeautifulSoup(pageContent, "html.parser")
                tabContentHtml = soup.select(".js-tab-content")[0]
                tabContent = tabContentHtml.get_text()

                self.parser.artist = artistName
                self.parser.songSource = songUrl
                self.parser.songTitle = "Placeholder Title"
                chartData = self.parser.parseChart(tabContent)

                self.log(str(chartData))
                self.log("----------\n")

                print("Parsed data for " + chartData.title)
