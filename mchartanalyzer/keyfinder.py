from decimal import *

from music21 import harmony, key, chord, roman

from utils import *

class KeyFinder:
    """
    Analyzes chord sequences for keys and other data
    """

    def __init__(self):
        self.keyListMajor = ['G-', 'D-', 'A-', 'E-', 'B-', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#']
        self.keyListMinor = ['e-', 'b-', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#']
        self.keyList = self.keyListMajor + self.keyListMinor

        self.keyLimit = 5
        self.lengthChordCursor = 4

        self._chordsPreDom = ['IV', 'iv', 'ii', 'II']

        ##### Chord progressions (Major)
        self.progsDominantMaj = [
            ['V', 'I'],
            ['V7', 'I'],
            ['viio', 'I'],
        ]

        self.progsPreDomMaj = []
        for prog in self.progsDominantMaj:
            for chord in self._chordsPreDom:
                newProg = [chord] + prog
                self.progsPreDomMaj.append(newProg)

        self.progsSpecificMaj = [
            ['vi', 'ii', 'V'],
            ['vi', 'ii', 'V7'],
            ['vi', 'II', 'V'],
            ['vi', 'II', 'V7'],
        ]

        self.chordsUnorderedMaj = [
            ['I', 'IV', 'V']
        ]

        #### Chord progressions (Minor)
        self.progsDominantMin = [
            ['V', 'i'],
            ['V7', 'i'],
            ['viio', 'i'],
        ]

        self.progsPreDomMin = []
        for prog in self.progsDominantMin:
            for chord in self._chordsPreDom:
                newProg = [chord] + prog
                self.progsPreDomMin.append(newProg)

        self.progsSpecificMin = [
            ['bVI', 'iio', 'V'],
            ['bVI', 'iio', 'V7'],
            ['bVI', 'ii', 'V'],
            ['bVI', 'ii', 'V7'],
            ['bVI', 'II', 'V'],
            ['bVI', 'II', 'V7'],
        ]

        self.chordsUnorderedMin = [
            ['i', 'iv', 'v'],
            ['i', 'iv', 'V'],
        ]

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
        listPossibleKeys = []

        if len(chordList) <= self.lengthChordCursor:
            possibleKeys = sortAndTrimDict(self._findPossibleKeys(chordList), self.keyLimit)

            for idx in range(len(chordList)):
                listPossibleKeys.append(possibleKeys)

            return listPossibleKeys
        else:
            maxIdx = len(chordList) - self.lengthChordCursor

            for idx, chordSymbol in enumerate(chordList):
                if idx < maxIdx:
                    cursorEndIdx = idx + 4
                    chordListSlice = chordList[idx:cursorEndIdx]
                    cursorPossibleKeys = self._findPossibleKeys(chordListSlice)
                    cursorPossibleKeys = sortAndTrimDict(cursorPossibleKeys, self.keyLimit)

                    if(idx == 0):
                        for startIndex in range(self.keyLimit):
                            listPossibleKeys.append(cursorPossibleKeys)
                    else:
                        listPossibleKeys.append(cursorPossibleKeys)

            return listPossibleKeys

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

        return sortAndTrimDict(possibleKeys, self.keyLimit)


    def _getRomanProgression(self, chordList, mKey):
        """
        Given a chordList and key, return a list of roman numeral chords.
        """
        chordListRoman = []

        for chordSymbol in chordList:
            formattedChordSymbol = convertToMusic21ChordSymbol(chordSymbol)
            mChord = harmony.ChordSymbol(formattedChordSymbol)
            romanObj = roman.romanNumeralFromChord(mChord, mKey)
            chordListRoman.append(substituteRomanChords(romanObj.figure))

        return chordListRoman

    def _detectProgressions(self, chordList, mKey):
        """
        Given a chordList and a key, determines if the chords fit the key in a better way.
        This is done through distinguishing chord movements like a ii-V-I.
        Returns a float, representing a score to be compared with other results.
        """
        chordListRoman = self._getRomanProgression(chordList, mKey)

        if mKey.mode == 'major':
            return self._detectMajorProgressions(chordListRoman)
        else:
            return 1

    def _detectMajorProgressions(self, romanChordList):
        """
        Detects important progressions in a major key.
        Returns a float, represengint a score to be compared with other results.
        """
        running_score = 0

        # if I, IV, and V are all present
        for prog in self.chordsUnorderedMaj:
            print('Comparing {0!s} and {1!s}'.format(prog, romanChordList))
            if self._areChordsInProgression(prog, romanChordList):
                running_score += 0.01
        
        return running_score

    def _areChordsInProgression(self, searchChordList, chordList):
        """
        Determines if chords in searchChordList exist in the chordList.
        Order doesn't matter. Returns a boolean.
        """
        if len(searchChordList) > len(chordList):
            return False

        chordsMatching = 0

        for needleChord in searchChordList:
            for haystackChord in chordList:
                if needleChord == haystackChord:
                    chordsMatching += 1

        if chordsMatching == len(searchChordList):
            return True
        else:
            return False

    def _areExactChordsInProgression(self, searchChordList, chordList):
        """
        Determines if chords in searchChordList exist in the chordList.
        Looks for the chords exactly the way they're listed.
        Returns a boolean.
        """
        ## idea: slice the chordList into subsets, and see if yours is in there...
        if len(searchChordList) > len(chordList):
            return False

        chordsMatching = 0

        for needleChord in searchChordList:
            for haystackChord in chordList:
                if needleChord == haystackChord:
                    chordsMatching += 1

        if chordsMatching == len(searchChordList):
            return True
        else:
            return False

    def _getChordFitScore(self, chordSymbol, mKey):
        """
        Determines if the given chord fits in the given key.
        Returns a floating point number.
        """
        formattedChordSymbol = convertToMusic21ChordSymbol(chordSymbol)
        chordPitches = harmony.ChordSymbol(formattedChordSymbol).pitches
        keyPitches = mKey.pitches[:-1] # removing last note in scale!
        chordTonesInKey = 0

        for chordPitch in chordPitches:
            for keyPitch in keyPitches:
                if keyPitch.pitchClass == chordPitch.pitchClass:
                    chordTonesInKey += 1

        return chordTonesInKey / len(chordPitches)
