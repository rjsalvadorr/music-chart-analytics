import re

from music21 import harmony
from music21 import converter
from music21 import key
from music21 import roman

from .objects.artistcalculations import ArtistCalculations
from .objects.chartcalculations import ChartCalculations
from .databasehandler import DatabaseHandler
from . import constants
from .filewriter import FileWriter

class ChartAnalyzer:
    """
    Analyzes the charts, and calculates the desired data for display.
    """

    filewriter = FileWriter()

    def __init__(self):
        self.dbHandler = DatabaseHandler()

    def _getChordProgressions(self, chordList):
        """
        Gets a series of four-chord progressions in the given chord list.
        Returns a dictionary with chord progressions as keys, and counts as values.
        """
        rawDict = dict()
        chordListLength = len(chordList)

        for idx, chordSym in enumerate(chordList):
            if idx < chordListLength - constants.NUM_CHORDS_IN_PROG:
                prog = ' '.join(chordList[idx:idx+constants.NUM_CHORDS_IN_PROG])
                if prog in rawDict:
                    rawDict[prog] = rawDict[prog] + 1
                else:
                    rawDict[prog] = 1

        return rawDict

    def _getMostCommonChords(self, chordList):
        """
        Gets the most common chord symbols in the given chord list.
        Returns a dictionary with chord symbols as keys, and counts as values.
        """
        rawDict = dict()

        for chordSym in chordList:
            if chordSym in rawDict:
                # if the chord is already in the dictionary, increment counter
                rawDict[chordSym] = rawDict[chordSym] + 1
            else:
                # if it's a new chord, create a new dict entry
                rawDict[chordSym] = 1

        return rawDict


    def _mergeCounterDictionary(self, chordDictMain, chordDict):
        # chordDictMain is considered the "trunk" that we're merging chordDict into.
        for chordSym in chordDict:
            if chordSym in chordDictMain:
                # if the chord is already in the dictionary, add both values together
                chordDictMain[chordSym] = chordDictMain[chordSym] + chordDict[chordSym]
            else:
                # if it's a new chord, create a new dict entry
                chordDictMain[chordSym] = chordDict[chordSym]

        return chordDictMain


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

    def _log(self, text):
        ChartAnalyzer.filewriter.log(text)


    def _convertChordSymbolToGeneral(self, chordSymbol, m21Key):
        """
        From a given key and chord symbol, return a chord symbol in roman numeral notation.
        For example: ?????
        """
        formattedChordSymbol = self._convertToMusic21ChordSymbol(chordSymbol)
        mChord = harmony.ChordSymbol(formattedChordSymbol)
        mKey = key.Key(m21Key)
        mRomanNumeral = roman.romanNumeralFromChord(mChord, mKey)

        regexRoot = r"[CDEFGAB](#{1,2}|b{1,2})?"
        rootlessChordSymbol = re.sub(regexRoot, '', chordSymbol)
        if rootlessChordSymbol == 'm':
            rootlessChordSymbol = ''

        genericChordSymbol = mRomanNumeral.romanNumeral + rootlessChordSymbol

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
        formattedChordSymbol = formattedChordSymbol.replace("maj", "")
        formattedChordSymbol = formattedChordSymbol.replace("Maj", "")
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
        chartCalcs.numSections = len(chartData.sections)

        return chartCalcs


    def _analyzeArtist(self, artistData):
        """
        Analyzes an artist. Returns an ArtistCalculations object.
        """
        artistCalcs = ArtistCalculations()
        artistDefinitiveChartCalcs = self.dbHandler.getDefinitiveChartCalcsForArtist(artistData.name)
        artistAllCharts = self.dbHandler.getAllChartsForArtist(artistData.name)

        allProgs = dict()
        allSections = dict()
        mostCommonKeys = dict()

        for chart in artistAllCharts:
            artistCalcs.numCharts += 1

        for chartCalc in artistDefinitiveChartCalcs:
            artistCalcs.numSongs += 1
            if chartCalc.key.lower().find("major") >= 0:
                artistCalcs.numMajorKeys += 1
            artistCalcs.numChords += chartCalc.numChords
            artistCalcs.numSections += chartCalc.numSections

            if chartCalc.key in mostCommonKeys:
                mostCommonKeys[chartCalc.key] = mostCommonKeys[chartCalc.key] + 1
            else:
                mostCommonKeys[chartCalc.key] = 1

            if chartCalc.chartData:
                songStruct = ' '.join(chartCalc.chartData.sections)
                if songStruct in allProgs:
                    allSections[songStruct] = allSections[songStruct] + 1
                else:
                    allSections[songStruct] = 1

            allProgs = self._mergeCounterDictionary(allProgs, self._getChordProgressions(chartCalc.chordsGeneral))

        artistCalcs.mostCommonKeys = self._trimDictionary(mostCommonKeys, constants.MOST_COMMON_CHORDS_LIMIT)
        artistCalcs.mostCommonChordProgressions = self._trimDictionary(allProgs, constants.MOST_COMMON_CHORDS_LIMIT)
        artistCalcs.mostCommonSongStructures = self._trimDictionary(allSections, constants.MOST_COMMON_CHORDS_LIMIT)
        artistCalcs.numMinorKeys = artistCalcs.numSongs - artistCalcs.numMajorKeys

        return artistCalcs


    def _dumpChartCalculationsToLog(self, artistData, songData, chartData, chartCalcs):
        logString = " source: " + chartData.source + "\n"
        logString += " artist: " + artistData.name + "\n"
        logString += " title: " + songData.title + "\n"
        logString += " sections: " + chartData.getSectionListString().replace(",", " ") + "\n"
        logString += " original chords: " + chartData.getChordListString().replace(",", " ") + "\n"
        logString += "\n"
        logString += " computed key: " + chartCalcs.key + "\n"
        logString += " computed key certainty: " + chartCalcs.keyAnalysisCertainty + "\n"
        logString += " computed chords: " + chartCalcs.getChordListString().replace(",", " ") + "\n"
        logString += " number of chords: " + str(chartCalcs.numChords) + "\n"
        logString += " number of sections: " + str(chartCalcs.numSections) + "\n"
        logString += "\n========================================\n"

        self._log(logString)


    def _dumpArtistCalculationsToLog(self, artistData, artistCalcs):
        logString = "\n============================================================\n"
        logString += " artist summary: " + artistData.name + "\n"
        logString += "============================================================\n"
        logString += " songs encountered: " + str(artistCalcs.numSongs) + "\n"
        logString += " total charts encountered: " + str(artistCalcs.numCharts) + "\n"
        logString += " songs in major: " + str(artistCalcs.numMajorKeys) + "\n"
        logString += " songs in minor: " + str(artistCalcs.numMinorKeys) + "\n"
        logString += " chords encountered: " + str(artistCalcs.numChords) + "\n"
        logString += " sections encountered: " + str(artistCalcs.numSections) + "\n"

        logString += "\n most common keys:\n"
        for keySym in artistCalcs.mostCommonKeys:
            logString += "    " + keySym + " - seen " + str(artistCalcs.mostCommonKeys[keySym]) + " times\n"

        logString += " most common chords (specific):\n"
        for chordSym in artistCalcs.mostCommonChordsSpecific:
            logString += "    " + chordSym + " - seen " + str(artistCalcs.mostCommonChordsSpecific[chordSym]) + " times\n"

        logString += " most common chords (generic):\n"
        for chordSym in artistCalcs.mostCommonChordsGeneric:
            logString += "    " + chordSym + " - seen " + str(artistCalcs.mostCommonChordsGeneric[chordSym]) + " times\n"

        logString += " most common chord progressions:\n"
        for progString in artistCalcs.mostCommonChordProgressions:
            logString += "    " + progString + " - seen " + str(artistCalcs.mostCommonChordProgressions[progString]) + " times\n"

        logString += " most common song structures:\n"
        for structString in artistCalcs.mostCommonSongStructures:
            logString += "    " + structString + " - seen " + str(artistCalcs.mostCommonSongStructures[structString]) + " times\n"

        logString += "\n avg. chords per song: " + str(artistCalcs.numChords / artistCalcs.numSongs) + "\n"
        logString += " avg. sections per song: " + str(artistCalcs.numSections / artistCalcs.numSongs) + "\n"

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

                totalMostCommonChordsSpec = self._mergeCounterDictionary(totalMostCommonChordsSpec, mcChordsSpec)
                totalMostCommonChordsGen = self._mergeCounterDictionary(totalMostCommonChordsGen, mcChordsGen)

                print("  - Analyzed " + songData.title)

            finalDictGen = self._trimDictionary(totalMostCommonChordsGen, constants.MOST_COMMON_CHORDS_LIMIT)
            finalDictSpec = self._trimDictionary(totalMostCommonChordsSpec, constants.MOST_COMMON_CHORDS_LIMIT)

            artistCalcs = self._analyzeArtist(artistData)
            artistCalcs.mostCommonChordsSpecific = finalDictSpec
            artistCalcs.mostCommonChordsGeneric = finalDictGen

            self._dumpArtistCalculationsToLog(artistData, artistCalcs)

            artistCalcs.artistData = artistData
            ChartAnalyzer.filewriter.writeArtistCalculations(artistCalcs)

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
