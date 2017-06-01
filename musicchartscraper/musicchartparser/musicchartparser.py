import re
from music21 import *
from .chartdata import ChartData

class MusicChartParser:
    """
    Parses data from a chord chart. Looks for information like title, key, chords, and structure.
    """

    sectionKeywords = ["intro", "verse", "prechorus", "pre-chorus", "pre chorus", "chorus", "bridge", "outro", "solo", "hook", "pre-hook", "coda", "middle 8"]

    chordSymbols = ["m", "M", "min", "maj", "dim"] # TRIADS
    chordSymbols.extend(["m7", "M7", "min7", "maj7", "dim7", "m7b5"]) # SEVENTHS
    chordSymbols.extend(["aug", "+", "7#5", "M7+5", "M7+", "m7+", "7+"]) # AUGMENTED
    chordSymbols.extend(["sus2", "sus4", "7sus4", "11", "sus4b9", "susb9"]) # SUSPENDED
    chordSymbols.extend(["6", "m6", "M6", "maj6", "6/7", "67", "6/9",  "69"]) # SIXTHS
    chordSymbols.extend(["9", "add9", "m9", "maj9", "M9", "7b9", "7#9"]) # NINTHS
    chordSymbols.extend(["11", "add11", "7#11", "m11"]) # ELEVENTHS
    chordSymbols.extend(["13", "add13", "M13", "m13", "maj13"]) # THIRTEENTHS
    chordSymbols.extend(["7b9", "7#9", "67", "6/7", "add2", "5"]) # ALTERATIONS

    def __init__(self):
        self._resetSongData()


    def _resetSongData(self):
        self.artist = None
        self.songTitle = None
        self.songSource = None
        self.chordList = []
        self.sectionList = []


    def _isChordSymbol(self, chordText):
        """
        Uses regex patterns to parse out chord symbols.
        """
        # We can't use word boundaries (/b) since # is not a word character!
        regexRoot = r"[CDEFGAB](#{1,2}|b{1,2})?"
        regexChords = r"("
        for idx, chordSymbol in enumerate(MusicChartParser.chordSymbols):
            if idx != 0:
                regexChords += r"|"
            regexChords += re.escape(chordSymbol)
        regexChords += r")"

        finalPattern = re.compile(regexRoot + regexChords + r"?(\/" + regexRoot + r")?")

        return finalPattern.fullmatch(chordText)


    def _removeSlashChordBass(self, chordSymbol):
        """
        Uses regex patterns to remove the bass note from slash chords
        """
        rePattern = re.compile(r"\/[CDEFGAB](#{1,2}|b{1,2})?$")
        return rePattern.sub("", chordSymbol)


    def _isSectionSymbol(self, text):
        """
        Uses regex patterns to parse out section markers
        """
        regexSections = r"[ \[]*("
        for idx, sectionKeyword in enumerate(MusicChartParser.sectionKeywords):
            if idx != 0:
                regexSections += r"|"
            regexSections += re.escape(sectionKeyword)
        regexSections += r")[ 1-9]*[ \]]*"

        finalPattern = re.compile(regexSections, re.IGNORECASE)

        return finalPattern.fullmatch(text)


    def _parseTitle(self, chartText):
        # Dummy data for now
        return "Dummy Data For The Win"


    def _parseKey(self, chartText):
        # Dummy data for now
        return "Cm"


    def _parseChords(self, chartText):
        chords = []

        tokens = chartText.split()
        for token in tokens:
            if self._isChordSymbol(token):
                chords.append(self._removeSlashChordBass(token))

        return chords


    def _parseSections(self, textLine):
        sections = []
        keywordExists = False
        keywordToken = None

        tokens = textLine.split()
        for token in tokens:
            if self._isSectionSymbol(token):
                keywordExists = True
                keywordToken = token

        if keywordExists:
            formmatedKeyword = keywordToken.upper()
            formmatedKeyword = formmatedKeyword.replace("[", "")
            formmatedKeyword = formmatedKeyword.replace("]", "")
            formmatedKeyword = formmatedKeyword.replace(" ", "")

            sections.append(formmatedKeyword)

        return sections


    def parseChart(self, chartText):
        chartData = ChartData()
        lines = chartText.splitlines()

        chartData.artist = self.artist
        chartData.title = self.songTitle
        chartData.source = self.songSource

        for line in lines:
            self.chordList.extend(self._parseChords(line))
            self.sectionList.extend(self._parseSections(line))

        chartData.chords = self.chordList
        chartData.sections = self.sectionList

        self._resetSongData()

        return chartData
