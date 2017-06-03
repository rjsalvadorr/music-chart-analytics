#!/usr/bin/env python
import sys
import os
import traceback

import random
import string

from mchartanalyzer.databasehandler import DatabaseHandler
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
print("##### DATA OBJECT TESTING #####\n")

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
print("##### DATABASE HANDLER TESTING #####\n")
dbHandler = DatabaseHandler()

# dbHandler.saveArtistData(newArtistData)
# dbHandler.saveSongData(newArtistData, newSongData)
# dbHandler.saveChartData(newSongData, newChartData)

artistResult1 = dbHandler.getArtistByName("HJGQQYQH")
artistResult2 = dbHandler.getArtistByName("SOMETHING_UNFINDABLE")
print(artistResult1)
print(artistResult2)