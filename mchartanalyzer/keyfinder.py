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
            return self._findPossibleKeys(chordList)
        else:
            maxIdx = len(chordList) - self.lengthChordCursor

            for idx, chordSymbol in enumerate(chordList):
                if idx <= maxIdx:
                    cursorEndIdx = idx + 4
                    chordListSlice = chordList[idx:cursorEndIdx]
                    print(chordListSlice)
                    cursorPossibleKeys = self._findPossibleKeys(chordListSlice)
                    totalPossibleKeys = Utils.mergeDictionaries(totalPossibleKeys, cursorPossibleKeys)

        return totalPossibleKeys

    def _findPossibleKeys(self, chordList):
        """
        Finds the possible keys for a given chord sequence.
        Returns an object like:
        {
          G major: 20,
          D major: 12,
          B minor: 5
        }
        Where the numbers represent a score, showing how well those chords fit in each key.

        Each chord symbol in key gets a + 1.
        Certain chord progressions will get more bonuses.

        """
        possibleKeys = dict()

        for keyRoot in self.keyList:
            diatonicKey = key.Key(keyRoot)
            chordSymbolsInKey = 0

            for chordSymbol in chordList:
                if self._isChordInKey(chordSymbol, diatonicKey):
                    chordSymbolsInKey += 1

            if chordSymbolsInKey > 1:
                keyName = diatonicKey.tonic.name + ' ' + diatonicKey.mode
                possibleKeys[keyName] = chordSymbolsInKey

        return possibleKeys

    def _isChordInKey(self, chordSymbol, mKey):
        """
        Determines if the given chord fits in the given key.
        """
        formattedChordSymbol = Utils.convertToMusic21ChordSymbol(chordSymbol)
        chordPitches = harmony.ChordSymbol(formattedChordSymbol).pitches
        keyPitches = mKey.pitches[:-1] # removing last note in scale!
        chordTonesInKey = 0;

        for chordPitch in chordPitches:
            for keyPitch in keyPitches:
                if keyPitch.pitchClass == chordPitch.pitchClass:
                    chordTonesInKey += 1

        if chordTonesInKey == len(chordPitches):
            return True
        else:
            return False
