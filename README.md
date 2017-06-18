# mChartAnalytics

Analyzes online chord charts for common traits and patterns.

## Project Goals

The goal of this project is to shed some light on the *sonic fingerprint* of certain musicians/bands (or at least their songwriters). The software will look for certain trends in their songs, such as structure and common chords and chord progressions. This data may give budding musicians a better idea of how a specific band approaches songwriting, or maybe even allow someone to mimic their favourite musicians!

## Overview

This repo has a few main parts: a **scraper**, **parser**, and **analyzer**. The scraper retrieves chord/tab sheets from certain websites, and makes it available for the parser to read and send to a database. The analyzer then takes that data and then plays around with it.

### Scraper

The scraper will be configured to look up a certain band's charts on webpages like [https://www.ultimate-guitar.com](https://www.ultimate-guitar.com). The scraper needs to go through the directory structure of the page in order to find the goods.

### Parser

The parser will read through all those charts and identify key features of the song:

- Structure/Form: Verses, choruses, etc. We're interested in the number of sections, and their order.
- Chords: The parser identifies the chords used in the song. Again, we're interested in the number of chords, their order, and number per section.
- Key: If a key is specified on the chart, this will be parsed out too.

### Analyzer

...

## Usage

...

## Development

This project uses Python 3.

### Dependencies

- beautifulsoup4
- requests
- music21
- PyYAML
- Sphinx

## Contact

Wanna know more, or feel like helping out? Contact me at rjsalvadorr@gmail.com!
