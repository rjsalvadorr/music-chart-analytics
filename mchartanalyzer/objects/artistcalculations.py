from .basedata import BaseDataObject

class ArtistCalculations(BaseDataObject):
    """
    Class encapsulating all the desired data about an artist/musician, after thorough analysis.
    """

    def __init__(self, databaseRow=None):
        BaseDataObject.__init__(self)

        self.artistId = 0
        self.numChords = 0 # TODO - remove?
        self.numSections = 0 # TODO - remove?
        self.numSongs = 0
        self.numCharts = 0
        self.numMajorKeys = 0
        self.numMinorKeys = 0

        self.mostCommonKeys = {}
        self.mostCommonChordsSpecific = {}
        self.mostCommonChordsGeneric = {}
        self.mostCommonChordProgressions = {}
        self.mostCommonSongStructures = {}

        if databaseRow:
            self.artistId = databaseRow[0]
            self.numChords = databaseRow[1]
            self.numSections = databaseRow[2]
            self.numSongs = databaseRow[3]
            self.numCharts = databaseRow[4]
            self.numMajorKeys = databaseRow[5]
            self.numMinorKeys = databaseRow[6]

            self.mostCommonKeys = self._convertStringToDict(databaseRow[7])
            self.mostCommonChordsSpecific = self._convertStringToDict(databaseRow[8])
            self.mostCommonChordsGeneric = self._convertStringToDict(databaseRow[9])
            self.mostCommonChordProgressions = self._convertStringToDict(databaseRow[10])
            self.mostCommonSongStructures = self._convertStringToDict(databaseRow[11])

    def __str__(self):
        stringRep = "ArtistCalculations { id=" + str(self.id) + ", "

        stringRep += "artistId=" + str(self.artistId) + ", "
        stringRep += "numChords=" + str(self.numChords) + ", "
        stringRep += "numSections=" + str(self.numSections) + ", "
        stringRep += "numSongs=" + str(self.numSongs) + ", "
        stringRep += "numCharts=" + str(self.numCharts) + ", "
        stringRep += "numMajorKeys=" + str(self.numMajorKeys) + ", "
        stringRep += "numMinorKeys=" + str(self.numMinorKeys) + ", "

        stringRep += "mostCommonKeys=" + self._convertDictToString(self.mostCommonKeys) + ", "
        stringRep += "mostCommonChordsSpecific=" + self._convertDictToString(self.mostCommonChordsSpecific) + ", "
        stringRep += "mostCommonChordsGeneric=" + self._convertDictToString(self.mostCommonChordsGeneric) + ", "
        stringRep += "mostCommonChordProgressions=" + self._convertDictToString(self.mostCommonChordProgressions) + ", "
        stringRep += "mostCommonSongStructures=" + self._convertDictToString(self.mostCommonSongStructures) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
