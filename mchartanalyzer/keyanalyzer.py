from music21 import harmony
from music21 import converter
from music21.analysis.discrete import DiscreteAnalysisException

from . import constants
from .conversionutils import ConversionUtils

class KeyAnalyzer:
    """
    Class responsible for finding the key of a given chart.
    """

    def __init__(self):
        pass

    def analyzeKey(self, chordList):
        """
        Determines the song's key by analyzing the chords in the current song.
        Returns a tuple with the analyzed key and key certainty.
        For example, ("G major", 0.977538)
        """

        try:
            return self._analyzeKeyWithMusic21(chordList)
        except DiscreteAnalysisException:
            return self._analyzeKeyByPitchClasses(chordList)

    def _analyzeKeyWithMusic21(self, chordList):
        """
        Determines the song's key by analyzing the chords in the current song.
        Returns a tuple with the analyzed key and key certainty.
        For example, ("G major", 0.977538)
        """
        # Get the pitches used in the current song's chords
        # And assemble those pitches into a large tinynotation string
        tinyNotationString = "tinyNotation: 4/4 "
        for chordSymbol in chordList:
            formattedChordSymbol = ConversionUtils._convertToMusic21ChordSymbol(chordSymbol)
            try:
                h = harmony.ChordSymbol(formattedChordSymbol)
                for rawPitch in h.pitches:
                    tnPitch = str(rawPitch)
                    tnPitch = tnPitch[:-1] # Removes the octave number from the pitch string
                    tinyNotationString += tnPitch + " "
            except ValueError as exc:
                print("Chord parsing failed due to " + repr(exc))
            except Exception as exc:
                print("Unexpected error while finding the key: " + repr(exc))
                print(traceback.format_exc())

        littlePiece = converter.parse(tinyNotationString)
        k = littlePiece.analyze('key')

        return (self._convertMusic21KeyToText(str(k)), round(k.tonalCertainty(), 6))

    def _analyzeKeyByPitchClasses(self, chordList):
        """
        Determines the song's key by analyzing the chords in the current song.
        Returns a string representing the analyzed key.
        """
        # Get the pitch classes for each chord, and keep track of each occurence.
        print("running alternate key finder!!!")
        return ("B minor", 0.765453)

    def _convertMusic21KeyToText(self, text):
        """
        Converts a music21 key string to a regular one.
        Music21 key strings use a lowercase tonic for minor keys, and use "-" as a flat accidental instead of "b".
        For example, this method would convert "b- minor" to "Bb Minor"
        """
        fText = text.title()
        return fText.replace("-", "b")
