import unittest

from music21 import harmony
from music21 import key

from keyfinder import KeyFinder

class KeyFinderTest(unittest.TestCase):

    def setUp(self):
        self.keyFinder = KeyFinder()

    def test_isChordInKey(self):
        testChord1 = 'C'
        testKey1 = key.Key('C')
        result1 = self.keyFinder._isChordInKey(testChord1, testKey1)
        self.assertEqual(result1, True)

        testChord2 = 'C#m'
        testKey2 = key.Key('C')
        result2 = self.keyFinder._isChordInKey(testChord2, testKey2)
        self.assertEqual(result2, False)

    def test_findPossibleKeys(self):
        testChords = ['G', 'Em', 'C', 'D']
        testResult = self.keyFinder._findPossibleKeys(testChords)

        print('findPossibleKeys()')
        print(testResult)

    def test_findKeys(self):
        testChordsRaw1 = "G Em C D"
        testChords1 = testChordsRaw1.split(" ")
        testChordsRaw2 = 'Bb Dm Eb Bb Bb Dm Eb Bb Bb Cm F Gm Dm Eb Bb Cm F Bb Bb Dm Eb Bb Bb Cm F Bb'
        testChords2 = testChordsRaw2.split(" ")

        print('findKeys()')

        testResult1 = self.keyFinder.findKeys(testChords1)
        testResult2 = self.keyFinder.findKeys(testChords2)

        print(testResult1)
        print(testResult2)

if __name__ == '__main__':
    unittest.main()
