
class ArtistData:
    """
    Class encapsulating all the desired data from the chord charts, after thorough analysis.
    """

    def __init__(self):
        # The properties listed below are good candidates for persistence and presentation
        self.artistName = ""
        self.sourceNames = ""
        self.sourceUrls = ""
        self.analysisTimestamp = ""

        self.numSongs = 0
        self.numMajorKeys = 0
        self.numMinorKeys = 0

        self.numChords = 0


    def __str__(self):
        stringRep = "artistName=" + self.artistName + "\n"
        stringRep += "sourceNames=" + ", ".join(self.sourceNames) + "\n"
        stringRep += "sourceUrls=" + "\n".join(self.sourceUrls) + "\n"
        stringRep += "analysisTimestamp=" + self.analysisTimestamp + "\n"
        stringRep += "numSongs=" + str(self.numSongs) + "\n"
        stringRep += "numMajorKeys=" + str(self.numMajorKeys) + "\n"
        stringRep += "numMinorKeys=" + str(self.numMinorKeys) + "\n"
        stringRep += "numChords=" + str(self.numChords) + "\n"

        return stringRep
