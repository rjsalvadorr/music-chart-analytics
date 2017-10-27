#!/usr/bin/env python
import sys
import os
import pprint # for console printing
import sqlite3

import yaml

from mchartanalyzer.databasehandler import DatabaseHandler
from mchartanalyzer.chartscraper import ChartScraper
from mchartanalyzer.chartanalyzer import ChartAnalyzer

# Loading configuration file
fileDir = os.path.dirname(os.path.realpath(__file__))
cfgFilePath = os.path.join(fileDir, 'config.yaml')
pPrinter = pprint.PrettyPrinter(indent=2, width=120)

initializeDatabaseEnabled = False
databasePurgeEnabled = False
forceAnalysisEnabled = False
testModeOverride = False

print("\n===============================================================")
print("        _____ _           _   _____         _                 ")
print("  _____|     | |_ ___ ___| |_|  _  |___ ___| |_ _ ___ ___ ___ ")
print(" |     |   --|   | .'|  _|  _|     |   | .'| | | |- _| -_|  _|")
print(" |_|_|_|_____|_|_|__,|_| |_| |__|__|_|_|__,|_|_  |___|___|_|  ")
print("                                             |___|            ")
print("===============================================================")
print(" mChartAnalyzer v0.0.1")
print("===============================================================")
print("sqlite3.version = " + sqlite3.version)
print("sqlite3.sqlite_version = " + sqlite3.sqlite_version + "\n")

# Reading program arguments
if len(sys.argv) > 0:
    for arg in sys.argv:
        if(arg.lower() == "--help" or arg.lower() == "-?" or arg.lower() == "?"):
            print("AVAILABLE FLAGS:\n")
            print("--initialize-database")
            print("    For local database use. Initializes the database by setting up the table structure.\n    If the database already exists, it destroys that first.\n")
            print("--purge-database")
            print("    For local database use. Removes all the data stored in the database.\n")
            print("--force-analysis")
            print("    Forces analysis of database contents.\n")
            print("--test-mode")
            print("    Runs mChartAnalyzer in test mode, overriding the configured mode.\n")
            print("--normal-mode")
            print("    Runs mChartAnalyzer in normal mode, overriding the configured mode.\n")
            print("")
            sys.exit(0)

        if(arg.lower() == "--purge-database"):
            print("Database purge enabled. All data from the database will be removed before scraping data.")
            databasePurgeEnabled = True

        if(arg.lower() == "--force-analysis"):
            print("Song analysis will be forced")
            forceAnalysisEnabled = True

        if(arg.lower() == "--initialize-database"):
            print("Database will be initialized.")
            initializeDatabaseEnabled = True

        if(arg.lower() == "--test-mode"):
            testModeOverride = True
            testModeEnabled = True

        if(arg.lower() == "--normal-mode"):
            testModeOverride = True
            testModeEnabled = False


# Reading from config file
try:
    stream = open(cfgFilePath, 'r')
    yamlData = yaml.load(stream)
    print("Gathering data for the following artists:")
    pPrinter.pprint(yamlData["artists"])
    print("")
except:
    print("YAML configuration failed to load!")
    raise
finally:
    stream.close()


dbHandler = DatabaseHandler()
mcScraper = ChartScraper()
mcAnalyzer = ChartAnalyzer()

if not testModeOverride:
    testModeEnabled = yamlData["testModeEnabled"]

if testModeEnabled:
    print("mChartAnalyzer will run in TEST MODE.")
else:
    print("mChartAnalyzer will run in NORMAL MODE.")

mcScraper.testModeEnabled = testModeEnabled
scrapeCooldownEnabled = yamlData["scrapeCooldownEnabled"]
mcScraper.scrapeCooldownEnabled = scrapeCooldownEnabled

if initializeDatabaseEnabled:
    dbHandler.initializeDatabase()
    print ("Database initialized!")

if databasePurgeEnabled:
    dbHandler.purgeDatabase()
    print ("Database purged!")

for artist in yamlData["artists"]:
    mcScraper.scrape(artist)

if forceAnalysisEnabled:
    mcAnalyzer.analyzeAllCharts()
else:
    mcAnalyzer.analyzeFreshCharts()

print("\nFinished!")
sys.exit(0)
