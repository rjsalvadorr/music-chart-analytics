from .basedata import BaseDataObject

class ArtistCalculations(BaseDataObject):
    """
    Class encapsulating all the desired data about an artist/musician, after thorough analysis.
    """

    def __init__(self):
        BaseDataObject.__init__(self)

        self.artistId = 0
        self.numSongs = 0
        self.numCharts = 0
        self.numMajorKeys = 0
        self.numMinorKeys = 0
        self.numChords = 0
        self.mostCommonChordsSpecific = 0
        self.mostCommonChordsGeneral = 0
        self.numChords = 0


    def __str__(self):
        stringRep = "ArtistCalculations { id=" + str(self.id) + ", "

        stringRep += "artistId=" + str(self.artistId) + ", "
        stringRep += "numSongs=" + str(self.numSongs) + ", "
        stringRep += "numCharts=" + str(self.numSongs) + ", "
        stringRep += "numMajorKeys=" + str(self.numMajorKeys) + ", "
        stringRep += "numMinorKeys=" + str(self.numMinorKeys) + ", "
        stringRep += "numChords=" + str(self.numChords) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
