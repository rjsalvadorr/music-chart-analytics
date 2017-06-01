import requests
import re

from bs4 import BeautifulSoup

from .scrapestrategy import ScrapeStrategy

class UltimateGuitarStrategy(ScrapeStrategy):
    def __init__(self):
        self.siteDomain = "ultimate-guitar.com"


    def _formatArtistName(self, artistName):
        formattedName = artistName.lower()
        formattedName = formattedName.replace(" ", "_")
        return formattedName


    def _getArtistUrl(self, artistName):
        formattedName = self._formatArtistName(artistName)
        return "https://www.ultimate-guitar.com/tabs/" + formattedName + "_chords_tabs.htm"


    def getSongUrls(self, artistName):
        # TODO - account for multiple pages!!
        artistUrl = self._getArtistUrl(artistName)
        resp = requests.get(artistUrl)
        print("(" + str(resp.status_code) + ") " + artistUrl)
        pageContent = resp.content
        soup = BeautifulSoup(pageContent, "html.parser")
        songUrls = []

        for urlTag in soup.select("td a"):
            hrefContent = urlTag["href"]
            if(hrefContent.find("crd") > 0):
                songUrls.append(hrefContent)

        return songUrls


    def getSongTitle(self, bSoup):
        titleTag = bSoup.select(".t_header .t_title h1")[0]
        rawTitle = titleTag.get_text()
        rePattern = re.compile(r"[ ]*chords", re.IGNORECASE)

        return rePattern.sub("", rawTitle)
