import pprint
import unittest

from music21 import harmony
from music21 import key

from keyfinder import KeyFinder

class KeyFinderTest(unittest.TestCase):

    def setUp(self):
        self.keyFinder = KeyFinder()
        self.pPrinter = pprint.PrettyPrinter(indent=2, width=120)

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
        testChords = ['G', 'Em', 'C', 'D']
        testResult = self.keyFinder._findPossibleKeys(testChords)

        self.pPrinter.pprint('findPossibleKeys()')
        self.pPrinter.pprint(testResult)

    def test_findKeys(self):
        testChordsRaw1 = "G Em C D"
        testChords1 = testChordsRaw1.split(" ")
        testChordsRaw2 = 'Bb Dm Eb Bb Bb Dm Eb Bb Bb Cm F Gm Dm Eb Bb Cm F Bb Bb Dm Eb Bb Bb Cm F Bb'
        testChords2 = testChordsRaw2.split(" ")

        self.pPrinter.pprint('findKeys()')

        testResult1 = self.keyFinder.findKeys(testChords1)
        testResult2 = self.keyFinder.findKeys(testChords2)

        self.pPrinter.pprint(testResult1)
        self.pPrinter.pprint(testResult2)

if __name__ == '__main__':
    unittest.main()
