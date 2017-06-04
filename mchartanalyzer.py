#!/usr/bin/env python
import sys
import os
import pprint # for console printing
import yaml

from mchartanalyzer.chartscraper import ChartScraper
from mchartanalyzer.databasehandler import DatabaseHandler

# Loading configuration file
fileDir = os.path.dirname(os.path.realpath(__file__))
cfgFilePath = os.path.join(fileDir, 'config.yaml')
pPrinter = pprint.PrettyPrinter(indent=2, width=120)

databasePurgeEnabled = False

if len(sys.argv) > 0:
    for arg in sys.argv:
        if(arg.lower() == "--help" or arg.lower() == "-?"):
            print("AVAILABLE FLAGS:")
            print("--purge-database")
            print("    Removes all the data stored in the database.\n")
            print("")
            sys.exit(0)

        if(arg.lower() == "--purge-database"):
            print("DATABASE PURGE ENABLED - All data from the database will be removed before scraping data.")
            databasePurgeEnabled = True

try:
    stream = open(cfgFilePath, 'r')
    yamlData = yaml.load(stream)
    print("\nCONFIGURATION SETTINGS:")
    pPrinter.pprint(yamlData)
    print("")
except:
    print("YAML configuration failed to load!")
    raise
finally:
    stream.close()

dbHandler = DatabaseHandler()
mcScraper = ChartScraper()

testModeEnabled = yamlData["testModeEnabled"]
mcScraper.testModeEnabled = testModeEnabled

scrapeCooldownEnabled = yamlData["scrapeCooldownEnabled"]
mcScraper.scrapeCooldownEnabled = scrapeCooldownEnabled

if databasePurgeEnabled:
    dbHandler.purgeDatabase()

for artist in yamlData["artists"]:
    mcScraper.scrape(artist)

sys.exit(0)
