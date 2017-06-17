from .basedata import BaseDataObject

class ArtistCalculations(BaseDataObject):
    """
    Class encapsulating all the desired data about an artist/musician, after thorough analysis.
    """

    def __init__(self):
        BaseDataObject.__init__(self)

        self.artistId = 0
        self.numChords = 0 # TODO - remove
        self.numSections = 0 # TODO - remove
        self.numSongs = 0
        self.numCharts = 0
        self.numMajorKeys = 0
        self.numMinorKeys = 0
        self.mostCommonKeys = {}
        self.mostCommonChordsSpecific = {}
        self.mostCommonChordsGeneric = {}
        self.mostCommonChordProgressions = {}
        self.mostCommonSongStructures = {}


    def __str__(self):
        stringRep = "ArtistCalculations { id=" + str(self.id) + ", "

        stringRep += "artistId=" + str(self.artistId) + ", "
        stringRep += "numSongs=" + str(self.numSongs) + ", "
        stringRep += "numCharts=" + str(self.numSongs) + ", "
        stringRep += "numMajorKeys=" + str(self.numMajorKeys) + ", "
        stringRep += "numMinorKeys=" + str(self.numMinorKeys) + ", "
        stringRep += "numChords=" + str(self.numChords) + ", "
        stringRep += "numSections=" + str(self.numSections) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
