#!/usr/bin/env python

from musicchartscraper.musicchartscraper import MusicChartScraper

mcScraper = MusicChartScraper()
mcScraper.scrape("Phish")
mcScraper.scrape("Michael Jackson")

print("Scraping complete!")
