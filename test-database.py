#!/usr/bin/env python
import sys
import os
import traceback

import random
import string

from mchartanalyzer.databasehandler import DatabaseHandler
from mchartanalyzer.chartscraper import ChartScraper
from mchartanalyzer.objects.artistdata import ArtistData
from mchartanalyzer.objects.songdata import SongData
from mchartanalyzer.objects.chartdata import ChartData

chordPool = ["Am", "Bdim", "C", "Dm", "Em", "F", "G", "G#dim", "E", "Bb7", "Ebmaj7", "Abmaj7"]
sectionPool = ["VERSE", "CHORUS", "BRIDGE", "PRE-CHORUS", "SOLO"]
domainPool = ["net", "com", "ca", "org"]

def getRandomChords():
    randomChords = []
    for _ in range(4):
        randomChords.append(random.choice(chordPool))
    return randomChords

def getRandomSections():
    randomSections = []
    for _ in range(4):
        randomSections.append(random.choice(sectionPool))
    return randomSections

def getRandomString():
    randomCharString = ""
    for _ in range(8):
        randomCharString += random.choice(string.ascii_lowercase)
    return randomCharString

def getRandomUrl():
    return "http://" + getRandomString() + "." + random.choice(domainPool) + "/thing.html"

###############################################################################
# DATA OBJECT TESTING
print("\n##### DATA OBJECT TESTING #####\n")

newArtistData = ArtistData()
newArtistData.name = getRandomString().upper()
for _ in range(4):
    newArtistData.sourceNames.append(getRandomString().title())
    newArtistData.sourceUrls.append(getRandomUrl())
print(newArtistData)
print("")


newSongData = SongData()
newSongData.title = getRandomString().upper()
print(newSongData)
print("")


newChartData = ChartData()
newChartData.source = getRandomUrl()
newChartData.chordsSpecific = getRandomChords()
newChartData.sections = getRandomSections()
newChartData.isNew = 1
print(newChartData)
print("")

###############################################################################
# DATABASE HANDLER TESTING
print("\n##### DATABASE HANDLER TESTING #####\n")
dbHandler = DatabaseHandler()
'''
dbHandler.saveArtistData(newArtistData)
dbHandler.saveSongData(newArtistData, newSongData)
dbHandler.saveChartData(newSongData, newChartData)
'''
artistResult1 = dbHandler.getArtistByName("HJGQQYQH")
artistResult2 = dbHandler.getArtistByName("SOMETHING_UNFINDABLE")
print(artistResult1)
print(artistResult2)

songRes = dbHandler.getSongByTitle("NEHFJPSJ")
print(songRes)

chartRes = dbHandler.getChartByUrl("http://lwwgfqxt.org/thing.html")
print(chartRes)

cScraper = ChartScraper()
testUrls = []
testUrls.append("http://lwwgfqxt.org/thing.html")
testUrls.append("http://vkojcxqa.org/thing.html")
testUrls.append("silly_value")

for earl in testUrls:
    validUrl = cScraper._isUrlValidTarget(earl)
    print("Is " + earl + " a valid URL? " + str(validUrl))
