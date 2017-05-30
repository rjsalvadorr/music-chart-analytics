#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

"""
Steps:

1. Get links for artist.
2. For each chord sheet, parse it for relevant data, and write the formatted chart out.
Potential filename format: artist-name_song-name_session-id.md
"""

class MusicChartScraper:
    def __init__(self):
        self.chordSheetLinks = []

    def scrape(self, artistName):
        """
        Scrapes websites for songs by a given artist.
        """

        # TODO - use strategies to get list of URLs for a specific artist on a specific page.

        self.chordSheetLinks.append("https://tabs.ultimate-guitar.com/m/marvin_gaye/whats_going_on_ver3_crd.htm");

        for sheetLink in self.chordSheetLinks:
            resp = requests.get(sheetLink)
            print("Status: " + str(resp.status_code))

            pageContent = resp.content
            soup = BeautifulSoup(pageContent, "html.parser")

            tabContentHtml = soup.select(".js-tab-content")[0]
            tabContent = tabContentHtml.get_text()

            print(tabContent)

            # TODO - run parser on each sheet, and extract features.

if __name__ == '__main__':
    # main method. This is where you're going to call the scraper.
    mcScraper = MusicChartScraper()
    mcScraper.scrape("placeholderValue")
