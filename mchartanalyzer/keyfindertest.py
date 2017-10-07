import pprint
import unittest

from music21 import harmony
from music21 import key

from keyfinder import KeyFinder

class KeyFinderTest(unittest.TestCase):

    def setUp(self):
        self.keyFinder = KeyFinder()
        self.pPrinter = pprint.PrettyPrinter(indent=2, width=120)

        self.testChordsMajor1 = 'G Em C D'.split(' ')

        self.testChordsMinor1 = 'Dm A Dm C F C Dm A7'.split(' ')

    def test_getChordFitScore(self):
        testChord1 = 'C'
        testKey1 = key.Key('C')
        result1 = self.keyFinder._getChordFitScore(testChord1, testKey1)
        self.assertEqual(result1, 1.00)

        testChord2 = 'C#m'
        testKey2 = key.Key('C')
        result2 = self.keyFinder._getChordFitScore(testChord2, testKey2)
        self.assertTrue(result2 > 0.32 and result2 < 0.34) # We're checking if result2 is approximately 0.333

    def test_findPossibleKeys(self):
        testResult = self.keyFinder._findPossibleKeys(self.testChordsMajor1)

        self.pPrinter.pprint('findPossibleKeys()')
        self.pPrinter.pprint(testResult)

    def test_getRomanProgression(self):
        testResult = self.keyFinder._getRomanProgression(self.testChordsMajor1, key.Key('G'))
        expResult = ['I', 'vi', 'IV', 'V']
        self.assertEqual(testResult, expResult)

        testChords2 = 'G Em C D7'.split(' ')
        testResult = self.keyFinder._getRomanProgression(testChords2, key.Key('G'))
        expResult = ['I', 'vi', 'IV', 'V7']
        self.assertEqual(testResult, expResult)

        testChords3 = 'G Em D F#dim'.split(' ')
        testResult = self.keyFinder._getRomanProgression(testChords3, key.Key('G'))
        expResult = ['I', 'vi', 'V', 'viio']
        self.assertEqual(testResult, expResult)

        testChords4 = 'G Em D F#dim7'.split(' ')
        testResult = self.keyFinder._getRomanProgression(testChords4, key.Key('G'))
        expResult = ['I', 'vi', 'V', 'viio7']
        self.assertEqual(testResult, expResult)

        testResult = self.keyFinder._getRomanProgression(testChords2, key.Key('C'))
        expResult = ['V', 'iii', 'I', 'II7']
        self.assertEqual(testResult, expResult)

        testResult = self.keyFinder._getRomanProgression(self.testChordsMinor1, key.Key('d'))
        expResult = ['i', 'V', 'i', 'bVII', 'III', 'bVII', 'i', 'V7']
        self.assertEqual(testResult, expResult)

    def test_detectProgressions(self):
        testResult = self.keyFinder._detectProgressions(self.testChordsMajor1, key.Key('G'))
        expResult = 0.01
        self.assertEqual(testResult, expResult)

    def test_detectMajorProgressions(self):
        testList = ['I', 'iv', 'IV', 'V']
        testResult = self.keyFinder._detectMajorProgressions(testList)
        expResult = 0.01
        self.assertEqual(testResult, expResult)

    def test_areChordsInProgression(self):
        testSearchList = ['I', 'IV', 'V']
        testList = ['I', 'iv', 'IV', 'V']
        testResult = self.keyFinder._areChordsInProgression(testSearchList, testList)
        expResult = True
        self.assertEqual(testResult, expResult)

        testSearchList = ['I', 'IV', 'V']
        testList = ['I', 'iv']
        testResult = self.keyFinder._areChordsInProgression(testSearchList, testList)
        expResult = False
        self.assertEqual(testResult, expResult)

        testSearchList = ['I', 'IV', 'V']
        testList = ['I', 'iv', 'ii', 'V']
        testResult = self.keyFinder._areChordsInProgression(testSearchList, testList)
        expResult = False
        self.assertEqual(testResult, expResult)

    def test_areExactChordsInProgression(self):
        testSearchList = ['V', 'I']
        testList = ['I', 'iv', 'IV', 'V']
        testResult = self.keyFinder._areExactChordsInProgression(testSearchList, testList)
        expResult = False
        self.assertEqual(testResult, expResult)

        testSearchList = ['V', 'I']
        testList = ['I', 'IV', 'V', 'I']
        testResult = self.keyFinder._areExactChordsInProgression(testSearchList, testList)
        expResult = True
        self.assertEqual(testResult, expResult)

    def test_findKeys(self):
        testChordsRaw2 = 'Bb Dm Eb Bb Bb Dm Eb Bb Bb Cm F Gm Dm Eb Bb Cm F Bb Bb Dm Eb Bb Bb Cm F Bb'
        testChords2 = testChordsRaw2.split(' ')

        self.pPrinter.pprint('findKeys()')

        testResult1 = self.keyFinder.findKeys(self.testChordsMajor1)
        testResult2 = self.keyFinder.findKeys(testChords2)

        self.pPrinter.pprint(testResult1)
        self.pPrinter.pprint(testResult2)

if __name__ == '__main__':
    unittest.main()
