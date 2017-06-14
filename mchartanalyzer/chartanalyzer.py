import re

from music21 import harmony
from music21 import converter
from music21 import key
from music21 import roman

from .objects.artistcalculations import ArtistCalculations
from .objects.chartcalculations import ChartCalculations
from .databasehandler import DatabaseHandler
from . import constants
from .logger import Logger

class ChartAnalyzer:
    """
    Analyzes the charts, and calculates the desired data for display.
    """

    logger = Logger()

    def __init__(self):
        self.dbHandler = DatabaseHandler()


    def _getMostCommonChordProgressions(self, numChords, chartData):
        return None


    def _getMostCommonChords(self, chordList):
        """
        Gets the most common chord symbols in the given chord list.
        Returns a dictionary with chord symbols as keys, and counts as values.
        Output is limited to the five most common chords.
        """
        rawDict = dict()
        returnDict = dict()


        for chordSym in chordList:
            if chordSym in rawDict:
                # if the chord is already in the dictionary, increment counter
                rawDict[chordSym] = rawDict[chordSym] + 1
            else:
                # if it's a new chord, create a new dict entry
                rawDict[chordSym] = 1

        return rawDict


    def _mergeMostCommonChords(self, dict1, dict2):
        # dict1 is considered the "trunk" that we're merging dict2 into.
        for chordSym in dict2:
            if chordSym in dict1:
                # if the chord is already in the dictionary, add both values together
                dict1[chordSym] = dict1[chordSym] + dict2[chordSym]
            else:
                # if it's a new chord, create a new dict entry
                dict1[chordSym] = dict2[chordSym]

        return dict1


    def _trimDictionary(self, oldDict, limit):
        newDict = dict()
        ctr = 0
        for dKey in sorted(oldDict, key=oldDict.get, reverse=True):
            ctr += 1
            newDict[dKey] = oldDict[dKey]
            if ctr >= limit:
                break

        return newDict


    def _getNumKeys(self, chartData):
        return None


    def _analyzeArtist(self, artistData, chartDataList):
        return None


    def _log(self, text):
        ChartAnalyzer.logger.log(text)


    def _convertChordSymbolToGeneral(self, chordSymbol, m21Key):
        """
        From a given key and chord symbol, return a chord symbol in roman numeral notation.
        For example: ?????
        """
        formattedChordSymbol = self._convertToMusic21ChordSymbol(chordSymbol)

        mChord = harmony.ChordSymbol(formattedChordSymbol)
        mKey = key.Key(m21Key)
        mRomanNumeral = roman.romanNumeralFromChord(mChord, mKey)

        genericChordSymbol = mRomanNumeral.romanNumeral + " " + mChord.commonName

        return genericChordSymbol.replace("-", "b")


    def _convertChordListToGeneral(self, chordList, keyString):
        """
        From a given key and chord symbol list, return a list of chord symbols in roman numeral notation.
        For example: ?????
        """
        genericChordList = []

        for chordSym in chordList:
            formattedKeyString = self._convertKeyTextToMusic21(keyString)
            genericChordList.append(self._convertChordSymbolToGeneral(chordSym, formattedKeyString))

        return genericChordList


    def _convertToMusic21ChordSymbol(self, text):
        """
        Converts regular chord symbols into ones that music21 understands.
        The main difference: the flat accidental is "-" on music21, not "b".
        For example, this method would convert "Bbm7" to "B-m7"
        """
        formattedChordSymbol = text.replace("b", "-")
        # Specific replacements below were added after certain music21 errors.
        # TODO - find a better way to avoid these issues!
        formattedChordSymbol = formattedChordSymbol.replace("-5", "b5")
        formattedChordSymbol = formattedChordSymbol.replace("-9", "b9")
        formattedChordSymbol = formattedChordSymbol.replace("maj", "Maj")
        formattedChordSymbol = formattedChordSymbol.replace("Maj7", "M7")
        formattedChordSymbol = formattedChordSymbol.replace("7sus4", "sus4")

        return formattedChordSymbol


    def _convertKeyTextToMusic21(self, text):
        """
        Converts a regular key string to a music21 key string.
        Music21 key strings use a lowercase tonic for minor keys, and use "-" as a flat accidental instead of "b".
        For example, this method would convert "Bb Minor" to "b- minor"
        """
        textParts = text.split(" ")
        fText = textParts[0].replace("b", "-")

        if textParts[1].upper() == "MINOR":
            fText = fText.lower()

        return fText


    def _convertMusic21KeyToText(self, text):
        """
        Converts a music21 key string to a regular one.
        Music21 key strings use a lowercase tonic for minor keys, and use "-" as a flat accidental instead of "b".
        For example, this method would convert "b- minor" to "Bb Minor"
        """
        fText = text.title()
        return fText.replace("-", "b")


    def _analyzeKey(self, chordList):
        """
        Determines the song's key by analyzing the chords in the current song.
        Returns a tuple with the analyzed key and key certainty.
        For example, ("G major", 0.977538)
        """
        # Get the pitches used in the current song's chords
        # And assemble those pitches into a large tinynotation string
        tinyNotationString = "tinyNotation: 4/4 "
        for chordSymbol in chordList:
            formattedChordSymbol = self._convertToMusic21ChordSymbol(chordSymbol)
            try:
                h = harmony.ChordSymbol(formattedChordSymbol)
                for rawPitch in h.pitches:
                    tnPitch = str(rawPitch)
                    tnPitch = tnPitch[:-1] # Removes the octave number from the pitch string
                    tinyNotationString += tnPitch + " "
            except ValueError as exc:
                print("Chord parsing failed due to " + repr(exc))
            except Exception as exc:
                print("UNEXPECTED ERROR: " + repr(exc))
                print(traceback.format_exc())

        littlePiece = converter.parse(tinyNotationString)
        k = littlePiece.analyze('key')

        return (self._convertMusic21KeyToText(str(k)), round(k.tonalCertainty(), 6))


    def _getBasicChartCalculations(self, chartData):
        """
        Analyzes a chart. Returns an ChartCalculations object.
        """
        chartCalcs = ChartCalculations()

        analyzedKey, analyzedKeyCertainty = self._analyzeKey(chartData.chordsSpecific)
        chartCalcs.key = analyzedKey
        chartCalcs.keyAnalysisCertainty = str(analyzedKeyCertainty)
        chartCalcs.chordsGeneral = self._convertChordListToGeneral(chartData.chordsSpecific, analyzedKey)
        chartCalcs.numChords = len(chartData.chordsSpecific)

        return chartCalcs


    def _analyzeArtist(self, artistData):
        """
        Analyzes an artist. Returns an ArtistCalculations object.
        """
        # artistCalcs = self.dbHandler.getBasicArtistStatistics(artistData)

        artistCalcs = ArtistCalculations()
        artistChartCalcs = self.dbHandler.getDefinitiveChartCalcsForArtist(artistData.name)
        artistAllCharts = self.dbHandler.getAllChartsForArtist(artistData.name)

        for chart in artistAllCharts:
            artistCalcs.numCharts += 1

        for chartCalc in artistChartCalcs:
            artistCalcs.numSongs += 1
            if chartCalc.key.lower().find("major") >= 0:
                artistCalcs.numMajorKeys += 1
            artistCalcs.numChords += chartCalc.numChords

        artistCalcs.numMinorKeys = artistCalcs.numSongs - artistCalcs.numMajorKeys

        return artistCalcs


    def _dumpChartCalculationsToLog(self, artistData, songData, chartData, chartCalcs):
        logString = "ARTIST: " + artistData.name + "\n"
        logString += "TITLE: " + songData.title + "\n"
        logString += "SECTIONS: " + chartData.getSectionListString().replace(",", " ") + "\n"
        logString += "ORIGINAL CHORDS: " + chartData.getChordListString().replace(",", " ") + "\n"
        logString += "\n"
        logString += "COMPUTED KEY: " + chartCalcs.key + "\n"
        logString += "COMPUTED KEY CERTAINTY: " + chartCalcs.keyAnalysisCertainty + "\n"
        logString += "COMPUTED CHORDS: " + chartCalcs.getChordListString().replace(",", " ") + "\n"
        logString += "# OF CHORDS: " + str(chartCalcs.numChords) + "\n"
        logString += "\n========================================\n"

        self._log(logString)


    def _dumpArtistCalculationsToLog(self, artistData, artistCalcs):
        logString = "\n============================================================\n"
        logString += " ARTIST: " + artistData.name + "\n"
        logString += "============================================================\n"
        logString += " SONGS: " + str(artistCalcs.numSongs) + "\n"
        logString += " CHARTS: " + str(artistCalcs.numCharts) + "\n"
        logString += " SONGS IN MAJOR: " + str(artistCalcs.numMajorKeys) + "\n"
        logString += " SONGS IN MINOR: " + str(artistCalcs.numMinorKeys) + "\n"
        logString += " CHORDS ENCOUNTERED: " + str(artistCalcs.numChords) + "\n"

        logString += " MOST COMMON CHORDS (SPECIFIC):\n"
        for chordSym in artistCalcs.mostCommonChordsSpecific:
            logString += "    " + chordSym + " - seen " + str(artistCalcs.mostCommonChordsSpecific[chordSym]) + " times\n"

        logString += " MOST COMMON CHORDS (GENERIC):\n"
        for chordSym in artistCalcs.mostCommonChordsGeneric:
            logString += "    " + chordSym + " - seen " + str(artistCalcs.mostCommonChordsGeneric[chordSym]) + " times\n"

        logString += "============================================================\n"

        self._log(logString)


    def _analyzeCharts(self, artistDataList):
        """
        Perform analysis on song charts associated to certain artists.
        """
        for artistData in artistDataList:
            print("\nAnalyzing data for " + artistData.name + "...")
            freshCharts = self.dbHandler.getAllChartsForArtist(artistData.name)
            totalMostCommonChordsSpec = dict()
            totalMostCommonChordsGen = dict()

            for freshChartData in freshCharts:
                songData = self.dbHandler.getSongById(freshChartData.songId)
                chartCalcs = self._getBasicChartCalculations(freshChartData)

                self.dbHandler.saveChartCalculationData(freshChartData, chartCalcs)
                self._dumpChartCalculationsToLog(artistData, songData, freshChartData, chartCalcs)

                mcChordsSpec = self._getMostCommonChords(freshChartData.chordsSpecific)
                mcChordsGen = self._getMostCommonChords(chartCalcs.chordsGeneral)

                totalMostCommonChordsSpec = self._mergeMostCommonChords(totalMostCommonChordsSpec, mcChordsSpec)
                totalMostCommonChordsGen = self._mergeMostCommonChords(totalMostCommonChordsGen, mcChordsGen)

                print("    Analyzed " + songData.title)

            finalDictGen = self._trimDictionary(totalMostCommonChordsGen, constants.MOST_COMMON_CHORDS_LIMIT)
            finalDictSpec = self._trimDictionary(totalMostCommonChordsSpec, constants.MOST_COMMON_CHORDS_LIMIT)

            artistCalcs = self._analyzeArtist(artistData)
            artistCalcs.mostCommonChordsSpecific = finalDictSpec
            artistCalcs.mostCommonChordsGeneric = finalDictGen

            self._dumpArtistCalculationsToLog(artistData, artistCalcs)

        print("\nData analyzed and persisted!")


    def analyzeFreshCharts(self):
        """
        Perform analysis on artists with fresh data.
        """
        freshArtists = self.dbHandler.getArtistsWithFreshCharts()

        if(len(freshArtists) == 0):
            print("No fresh data! No analysis will be done.")
            return

        self._analyzeCharts(freshArtists)


    def analyzeAllCharts(self):
        """
        Perform analysis on all artists.
        """
        allArtists = self.dbHandler.getAllArtists()
        self._analyzeCharts(allArtists)
