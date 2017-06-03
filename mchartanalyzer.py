#!/usr/bin/env python
import os
import pprint # for console printing
import yaml
from mchartanalyzer.chartscraper import ChartScraper

# Loading configuration file
fileDir = os.path.dirname(os.path.realpath(__file__))
cfgFilePath = os.path.join(fileDir, 'config.yaml')
pPrinter = pprint.PrettyPrinter(indent=2, width=120)

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

mcScraper = ChartScraper()

if yamlData["testModeEnabled"]:
    mcScraper.testModeEnabled = True

for artist in yamlData["artists"]:
    mcScraper.scrape(artist)
