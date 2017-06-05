from music21 import harmony
from music21 import converter
from music21 import key

from .objects.artistcalculations import ArtistCalculations
from .objects.chartcalculations import ChartCalculations
from .databasehandler import DatabaseHandler

class ChartAnalyzer:
    """
    Analyzes the charts, and calculates the desired data for display.
    """
    def __init__(self):
        self.dbHandler = DatabaseHandler()


    def _getNumKeys(self, chartDataList):
        return None


    def _getNumMajorKeys(self, chartDataList):
        return None


    def _getMostCommonChordProgressions(self, numChords, chartData):
        return None


    def _getMostCommonChords(self, chartData):
        return None


    def _getNumKeys(self, chartData):
        return None


    def _analyzeArtist(self, artistData, chartDataList):
        return None


    def _convertChordSymbolToGeneral(self, chordSymbol, m21Key):
        """
        From a given key and chord symbol, return a chord symbol in roman numeral notation.
        For example: ?????
        """
        formattedChordSymbol = self._convertToMusic21ChordSymbol(chordSymbol)

        h = harmony.ChordSymbol(formattedChordSymbol)
        h.key = key.Key(m21Key)

        # print("chordSymbol=" + chordSymbol + ", formattedChordSymbol=" + formattedChordSymbol + ", m21Key=" + m21Key)
        # print("h.romanNumeral.romanNumeral=" + h.romanNumeral.romanNumeral)
        # print("h.romanNumeral=" + str(h.romanNumeral))

        genericChordSymbol = h.romanNumeral.romanNumeral

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


    def _analyzeChart(self, chartData):
        """
        Analyzes a chart,
        """
        chartCalcs = ChartCalculations()

        analyzedKey, analyzedKeyCertainty = self._analyzeKey(chartData.chordsSpecific)
        chartCalcs.key = analyzedKey
        chartCalcs.keyAnalysisCertainty = str(analyzedKeyCertainty)
        chartCalcs.chordsGeneral = self._convertChordListToGeneral(chartData.chordsSpecific, analyzedKey)

        return chartCalcs


    def analyzeFreshCharts(self):
        freshArtists = self.dbHandler.getArtistsWithFreshCharts()

        for artistData in freshArtists:
            print("")
            print(artistData)

            freshCharts = self.dbHandler.getFreshChartsForArtist(artistData.name)

            for freshChartData in freshCharts:
                print("")
                print(freshChartData)

                chartCalcs = self._analyzeChart(freshChartData)
                print(chartCalcs)
