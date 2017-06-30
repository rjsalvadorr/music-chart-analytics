#!/usr/bin/env python
import sys
import os
import traceback

from mchartanalyzer.filewriter import FileWriter
from mchartanalyzer.chartparser import ChartParser

filewriter = FileWriter(testMode=True)
parser = ChartParser()

filenames = []
filenames.append("chart1.txt")
filenames.append("chart2.txt")
filenames.append("chart3.txt")
filenames.append("chart4.txt")
filenames.append("chart5.txt")
filenames.append("chart6.txt")
filenames.append("chart7.txt")
filenames.append("chart8.txt")
filenames.append("chart9.txt")

chordSymbols = ["Bb", "F#", "Cm7", "Ebm7b5", "F#dim", "C#dim/G", "Abmaj7/Eb", "Blugh", "Lorem", "C5345345"]
slashChordSymbols = ["Bb", "C#dim/G", "Some/thing/d", "Abmaj7/Eb"]

moduleDir = os.path.dirname(os.path.realpath(__file__))
inputDir = os.path.join(moduleDir, "test")

print("Testing!")
print("")

# CHORD SYMBOL PARSING
for chordSym in chordSymbols:
    result = parser._isChordSymbol(chordSym)
    resString = "YEP" if result else "NOPE"
    print("Is " + chordSym + " a chord symbol? " + resString)
print("")

# SLASH CHORD SYMBOL PARSING
for chordSym in slashChordSymbols:
    result = parser._removeSlashChordBass(chordSym)
    print(chordSym + " -> " + result)
print("")

# FILE PARSING
for idx, filename in enumerate(filenames):
    filePath = os.path.join(inputDir, filename)
    try:
        with open(filePath, 'r') as inFile:
            chartLines = inFile.read()

        parser.artist = "Placeholder Artist"
        parser.songSource = "http://www.whatever.io/shoop.html"
        parser.songTitle = "Placeholder Title (" + str(idx + 1) + ")"
        chartData = parser.parseChart(chartLines)

        filewriter.log(str(chartData))
        filewriter.log("----------\n")

    except IOError as exc:
        print("ERROR! Unable to copy file. " + repr(exc))
    except Exception as exc:
        print("Unexpected error: " + repr(exc))
        print(traceback.format_exc())

print("Testing complete!")
