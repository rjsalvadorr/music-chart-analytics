import collections
import decimal
import re
import copy

from music21 import harmony, key, chord, roman

from .utils import *

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
        self.baseChordProgWeight = 0.15
        self.functionalityScoreAdjust = 150
        self.smallKeyLimit = 4

        self._chordsPreDomMaj = ['IV', 'ii', 'II']
        self._chordsPreDomMin = ['iv', 'iio', 'II', 'ii']

        ##### Chord progressions (Major)
        self.progsDominantMaj = [
            ['V', 'I'],
            ['V7', 'I'],
            ['viio', 'I'],
        ]

        self.progsPreDomMaj = []
        for prog in self.progsDominantMaj:
            for chord in self._chordsPreDomMaj:
                newProg = [chord] + prog
                self.progsPreDomMaj.append(newProg)
        # print(self.progsPreDomMaj)

        self.progsSpecificMaj = [
            ['vi', 'ii', 'V'],
            ['vi', 'ii', 'V7'],
            ['vi', 'II', 'V'],
            ['vi', 'II', 'V7'],
        ]

        self.progsUnorderedMaj = [
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
            for chord in self._chordsPreDomMin:
                newProg = [chord] + prog
                self.progsPreDomMin.append(newProg)
        # print(self.progsPreDomMin)

        self.progsSpecificMin = [
            ['bVI', 'iio', 'V'],
            ['bVI', 'iio', 'V7'],
            ['bVI', 'ii', 'V'],
            ['bVI', 'ii', 'V7'],
            ['bVI', 'II', 'V'],
            ['bVI', 'II', 'V7'],
        ]

        self.progsUnorderedMin = [
            ['i', 'iv', 'v'],
            ['i', 'iv', 'V'],
        ]

    def findKeys(self, chordList, strict=False):
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
        keysInPiece = []

        if len(chordList) <= self.lengthChordCursor:
            possibleKeys = self._findPossibleKeys(chordList)
            for dKey, value in possibleKeys.items():
                # print('Key = {!s}, Value = {!s}'.format(dKey, value))
                mKey = key.Key(dKey)
                possibleKeys[dKey] += self._detectProgressions(chordList, mKey)
            possibleKeys = sortAndTrimDict(possibleKeys, self.keyLimit)

            for idx in range(len(chordList)):
                listPossibleKeys.append(copy.deepcopy(possibleKeys))
        else:
            maxIdx = len(chordList) - self.lengthChordCursor

            for idx, chordSymbol in enumerate(chordList):
                if idx < maxIdx:
                    cursorEndIdx = idx + 4
                    chordListSlice = chordList[idx:cursorEndIdx]
                    cursorPossibleKeys = self._findPossibleKeys(chordListSlice)
                    for dKey, value in cursorPossibleKeys.items():
                        # print('Key = {!s}, Value = {!s}'.format(dKey, value))
                        mKey = key.Key(dKey)
                        cursorPossibleKeys[dKey] += self._detectProgressions(chordListSlice, mKey)
                    cursorPossibleKeys = sortAndTrimDict(cursorPossibleKeys, self.keyLimit)

                    if(idx == 0):
                        for startIndex in range(self.keyLimit):
                            listPossibleKeys.append(copy.deepcopy(cursorPossibleKeys))
                    else:
                        listPossibleKeys.append(cursorPossibleKeys)

        currentKey = ''
        for idx, possibleKey in enumerate(listPossibleKeys):
            indexKey, indexKeyLikelihood = possibleKey.popitem(False)
            if indexKey != currentKey:
                keyTuple = (indexKey, indexKeyLikelihood, idx + 1)
                keysInPiece.append(keyTuple)
            currentKey = indexKey
        # print('chordList length = {}\tlistPossibleKeys length = {}'.format(len(chordList), len(listPossibleKeys)))

        if strict == False:
            # Remove key sections that are smaller than 4 measures
            oldList = keysInPiece
            keysInPiece = []
            print('chordList length = {}'.format(len(chordList)))
            for idx, keyInPiece in enumerate(oldList):
                if idx == len(oldList) - 1:
                    duration = len(chordList) - (keyInPiece[2] - 1)
                else:
                    duration = oldList[idx + 1][2] - keyInPiece[2]

                print('currentKey = {}, keyInPiece = {!s}, duration = {}'.format(currentKey, keyInPiece, duration))

                if len(keysInPiece) > 0:
                    previousKey = keysInPiece[-1][0]
                else:
                    previousKey = ''

                if (duration == len(chordList) or duration > self.smallKeyLimit) and previousKey != keyInPiece[0]:
                    keysInPiece.append(keyInPiece)
                    
        return keysInPiece

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

            returnSymbol = substituteRomanChords(romanObj.figure)
            rgxFilterWhitelist = re.compile(r'[b#]?[IV]*[iv]*o?7?')
            rgxFilterBlacklist = re.compile(r'[-#]?[iv]+7')

            filterMatchWhitelist = rgxFilterWhitelist.fullmatch(returnSymbol)
            filterMatchBlacklist = rgxFilterBlacklist.fullmatch(returnSymbol)
            # print('figure= {}\tfSymbol = {}\tnumeral = {}\tmatch = {!s}'.format(romanObj.figure, returnSymbol, convertRomanScaleDegree(romanObj.romanNumeral), filterMatchWhitelist))

            if filterMatchWhitelist == None or filterMatchBlacklist:
                returnSymbol = convertRomanScaleDegree(romanObj.romanNumeral)

            chordListRoman.append(returnSymbol)

        return chordListRoman

    def _detectProgressions(self, chordList, mKey):
        """
        Given a chordList and a key, determines if the chords fit the key in a better way.
        This is done through distinguishing chord movements like a ii-V-I.
        Returns a float, representing a score to be compared with other results.
        """
        romanChordList = self._getRomanProgression(chordList, mKey)

        isMajor =  mKey.mode == 'major'
        unorderedProg = self.progsUnorderedMaj if isMajor else self.progsUnorderedMin
        preDominantProg = self.progsPreDomMaj if isMajor else self.progsPreDomMin
        dominantProg = self.progsDominantMaj if isMajor else self.progsDominantMin

        running_score = 0
        for romanChord in romanChordList:
            rn = roman.RomanNumeral(romanChord)
            running_score += (rn.functionalityScore / 100) ** 3 * self.baseChordProgWeight
        running_score = running_score / len(romanChordList)

        # print('{!s} in {!s} = {!s}'.format(chordList, mKey, romanChordList))
        # print('progression score after rn.functionalityScore = {}'.format(running_score))

        for prog in unorderedProg:
            if self._areChordsInProgression(prog, romanChordList):
                running_score += self.baseChordProgWeight

        for prog in preDominantProg:
            if self._areExactChordsInProgression(prog, romanChordList):
                running_score += self.baseChordProgWeight * 3

        for prog in dominantProg:
            if self._areExactChordsInProgression(prog, romanChordList):
                running_score += self.baseChordProgWeight * 2

        # print('progression score after everything else = {}\n'.format(running_score))

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
        if len(searchChordList) > len(chordList):
            return False

        searchChordsLength = len(searchChordList)
        maxIndex = len(chordList) - searchChordsLength

        for idx in range(maxIndex + 1):
            sliceIdx = idx + searchChordsLength
            chordListSlice = chordList[idx:sliceIdx]
            if searchChordList == chordListSlice:
                return True

        return False

    def _getChordFitScore(self, chordSymbol, mKey):
        """
        Determines if the given chord fits in the given key.
        Returns a floating point number between 0 and 1.
        1.0 means that all the chord tones fit in the key.
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
