import requests
from bs4 import BeautifulSoup

"""
Steps:

1. Get links for artist.
2. For each chord sheet, parse it for relevant data, and write the formatted chart out.
Potential filename format: artist-name_song-name_session-id.md
"""

class LilypondFileBuilder:
    def __init__(self):
        self.chordSheetLinks = []

    def scrape(artistName):
    """
    Scrapes websites for songs by a given artist.
    """
        chordSheetLinks.append("https://tabs.ultimate-guitar.com/m/marvin_gaye/whats_going_on_ver3_crd.htm");

        for sheetLink in chordSheetLinks:
            resp = requests.get(sheetLink)
            print("Status: " + str(resp.status_code))

            pageContent = resp.content
            soup = BeautifulSoup(pageContent, "html.parser")

            tabContentHtml = soup.select(".js-tab-content")[0]
            tabContent = tabContentHtml.get_text()

            print(tabContent)
