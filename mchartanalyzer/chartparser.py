import re
from music21 import harmony
from music21 import converter

from .logger import Logger
from .objects.chartdata import ChartData
from .objects.artistdata import ArtistData

class ChartParser:
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

    logger = Logger()


    def __init__(self):
        self.artistData = None

        self._resetSongData()



    def _resetSongData(self):
        self.chordList = []
        self.sectionList = []

        self.analyzedKey = None
        self.analyzedKeyCertainty = None


    def log(self, text):
        ChartParser.logger.log(text)


    def _isChordSymbol(self, text):
        """
        Returns true if the given text is a chord symbol.
        """
        # We can't use word boundaries (/b) since # is not a word character!
        regexRoot = r"[CDEFGAB](#{1,2}|b{1,2})?"
        regexChords = r"("
        for idx, chordSymbol in enumerate(ChartParser.chordSymbols):
            if idx != 0:
                regexChords += r"|"
            regexChords += re.escape(chordSymbol)
        regexChords += r")"

        finalPattern = re.compile(regexRoot + regexChords + r"?(\/" + regexRoot + r")?")

        return finalPattern.fullmatch(text)


    def _removeSlashChordBass(self, chordSymbol):
        """
        Remove the bass note from slash chord symbols. For example, this function would take "Gm7/Bb" and return "Gm7".
        """
        rePattern = re.compile(r"\/[CDEFGAB](#{1,2}|b{1,2})?$")
        return rePattern.sub("", chordSymbol)


    def _isSectionSymbol(self, text):
        """
        Returns true if the given text is probably a section marking, such as "Chorus" or "Verse".
        """
        regexSections = r"[ \[]*("
        for idx, sectionKeyword in enumerate(ChartParser.sectionKeywords):
            if idx != 0:
                regexSections += r"|"
            regexSections += re.escape(sectionKeyword)
        regexSections += r")[ 1-9]*[ \]]*"

        finalPattern = re.compile(regexSections, re.IGNORECASE)

        return finalPattern.fullmatch(text)


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


    def _convertMusic21Key(self, text):
        """
        Converts a music21 key string to a regular one.
        Music21 key strings use a lowercase tonic for minor keys, and use "-" as a flat accidental instead of "b".
        For example, this method would convert "b- minor" to "Bb Minor"
        """
        fText = text.title()
        return fText.replace("-", "b")


    def _analyzeKey(self):
        """
        Determines the song's key by analyzing the chords in the current song.
        """
        # Get the pitches used in the current song's chords
        # And assemble those pitches into a large tinynotation string
        tinyNotationString = "tinyNotation: 4/4 "
        for chordSymbol in self.chordList:
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

        self.analyzedKeyCertainty = str(round(k.tonalCertainty(), 5))

        return self._convertMusic21Key(str(k))


    def _parseChords(self, chartText):
        """
        Parses the chord chart for chord symbols, such as "Gmaj7" or "F#m7b5"
        """
        chords = []

        tokens = chartText.split()
        for token in tokens:
            if self._isChordSymbol(token):
                chords.append(self._removeSlashChordBass(token))

        return chords


    def _parseSections(self, textLine):
        """
        Parses the chord chart for section markings, such as "Chorus" or "Verse".
        """
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


    def parseChart(self, songTitle, chartSourceUrl, chartContent):
        """
        Core function of the Parser.
        Calls a series of internal parsing methods to extract data from a chord chart.
        """
        chartData = ChartData()
        lines = chartContent.splitlines()

        chartData.artist = self.artistData.artistName
        chartData.title = songTitle.upper()
        chartData.source = chartSourceUrl

        for line in lines:
            self.chordList.extend(self._parseChords(line))
            self.sectionList.extend(self._parseSections(line))

        chartData.chordsSpecific = self.chordList
        chartData.key = self._analyzeKey()
        chartData.keyAnalysisCertainty = self.analyzedKeyCertainty
        chartData.sections = self.sectionList

        self._resetSongData()
        self.log(chartData.toLogString())
        self.log("----------\n")

        print("Parsed data for " + chartData.title)


    def setArtistData(self, name, sources, artistSourceUrls):
        """
        Sets the current artist info for the parser.
        """
        freshArtistData = ArtistData()
        freshArtistData.artistName = name
        freshArtistData.sourceNames = sources
        freshArtistData.soureUrls = artistSourceUrls

        self.artistData = freshArtistData


    def analyzeData(self):
        """
        Calls a series of internal analysis methods to analyze data and get it ready for persistence.
        """
        return 0
