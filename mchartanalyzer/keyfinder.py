from decimal import *

from music21 import harmony
from music21 import key

from utils import Utils

class KeyFinder:
    """
    Analyzes chord sequences for keys and other data
    """

    def __init__(self):
        self.keyListMajor = ['G-', 'D-', 'A-', 'E-', 'B-', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#']
        self.keyListMinor = ['e-', 'b-', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#']
        self.keyList = self.keyListMajor + self.keyListMinor

        self.keyLimit = 4
        self.lengthChordCursor = 4

    def findKeys(self, chordList):
        """
        Find the key(s) for the given chord sequence.
        Returns an object like:
        {
          G major: '1-34',
          D major: '35-65'
        }
        Where the numbers represent where in the sequence each key starts.
        """
        totalPossibleKeys = dict()

        if len(chordList) <= self.lengthChordCursor:
            return Utils.sortAndTrimDict(self._findPossibleKeys(chordList), self.keyLimit)
        else:
            maxIdx = len(chordList) - self.lengthChordCursor

            for idx, chordSymbol in enumerate(chordList):
                if idx < maxIdx:
                    cursorEndIdx = idx + 4
                    chordListSlice = chordList[idx:cursorEndIdx]
                    cursorPossibleKeys = self._findPossibleKeys(chordListSlice)
                    totalPossibleKeys = Utils.mergeDictionaries(totalPossibleKeys, cursorPossibleKeys)

        return Utils.sortAndTrimDict(totalPossibleKeys, self.keyLimit)

    def _findPossibleKeys(self, chordList):
        """
        Finds the possible keys for a given chord sequence.
        Returns an object like:
        {
          G major: 0.97562,
          D major: 0.87234,
          B minor: 0.75324
        }
        Where the numbers represent a score, showing how well those chords fit in each key.
        A value of 1.0 means that all the chords fit in that key.
        """
        possibleKeys = dict()

        for keyRoot in self.keyList:
            diatonicKey = key.Key(keyRoot)
            totalChordFitScore = 0

            for chordSymbol in chordList:
                chordFitScore = self._getChordFitScore(chordSymbol, diatonicKey)
                totalChordFitScore += chordFitScore

            avgChordFitScore = totalChordFitScore / len(chordList)
            possibleKeys[keyRoot] = avgChordFitScore

        return Utils.sortAndTrimDict(possibleKeys, self.keyLimit)

    def _detectProgressions(self, chordList, mKey):
        """
        Given a chordList and a key, determines if the chords fit the key in a better way.
        This is done through distinguishing chord movements like a ii-V-I.
        Returns an integer, representing a score to be compared with other results.
        """
        pass

    def _getChordFitScore(self, chordSymbol, mKey):
        """
        Determines if the given chord fits in the given key.
        Returns a floating point number.
        """
        formattedChordSymbol = Utils.convertToMusic21ChordSymbol(chordSymbol)
        chordPitches = harmony.ChordSymbol(formattedChordSymbol).pitches
        keyPitches = mKey.pitches[:-1] # removing last note in scale!
        chordTonesInKey = 0

        for chordPitch in chordPitches:
            for keyPitch in keyPitches:
                if keyPitch.pitchClass == chordPitch.pitchClass:
                    chordTonesInKey += 1

        return chordTonesInKey / len(chordPitches)
