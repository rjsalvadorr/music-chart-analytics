import urllib.parse
import re

import requests
from bs4 import BeautifulSoup

from .scrapestrategy import ScrapeStrategy

class UltimateGuitarStrategy(ScrapeStrategy):
    def __init__(self):
        self.siteDomain = "ultimate-guitar.com"
        self.siteDomainRoot = "http://ultimate-guitar.com"


    def _formatArtistName(self, artistName):
        formattedName = artistName.lower()
        formattedName = formattedName.replace(" ", "_")
        return formattedName


    def getSourceName(self):
        return "Ultimate Guitar"


    def getArtistUrl(self, artistName):
        formattedName = self._formatArtistName(artistName)
        return "https://www.ultimate-guitar.com/tabs/" + formattedName + "_chords_tabs.htm"


    def getSongUrls(self, artistUrl):
        """
        Gets the song URLs from an artist chord chart page.
        If there are multiple pages available, this method will call itself for the next available page.
        """
        resp = requests.get(artistUrl)
        # print("(" + str(resp.status_code) + ") " + artistUrl)
        pageContent = resp.content
        soup = BeautifulSoup(pageContent, "html.parser")
        songUrls = []

        for urlTag in soup.select("td a"):
            hrefContent = urlTag["href"]
            if hrefContent.find("crd") >= 0 and hrefContent.find("album_crd") is -1:
                songUrls.append(hrefContent)

        for urlTag in soup.select("td a.ys"):
            navLinkText = urlTag.get_text()
            navLinkUrl = urlTag["href"]
            navLinkUrlAbs = urllib.parse.urljoin(self.siteDomainRoot, navLinkUrl)

            if navLinkText.lower().find("next") >= 0:
                songUrls.extend(self.getSongUrls(navLinkUrlAbs))

        return songUrls


    def getSongUrlsForArtist(self, artistName):
        """
        Gets the chart URLs for a given artist.
        """
        artistUrl = self.getArtistUrl(artistName)
        songUrls = self.getSongUrls(artistUrl)

        return songUrls


    def getSongTitle(self, bSoup):
        titleTag = bSoup.select(".t_header .t_title h1")[0]
        rawTitle = titleTag.get_text()
        rePattern = re.compile(r"[ ]*chords", re.IGNORECASE)

        return rePattern.sub("", rawTitle)
