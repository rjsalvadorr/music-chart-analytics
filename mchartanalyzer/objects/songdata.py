from .basedata import BaseDataObject

class SongData(BaseDataObject):
    """
    Class encapsulating basic information about a song.
    """

    def __init__(self, databaseRow=None):
        BaseDataObject.__init__(self)

        self.artistId = 0
        self.title = ""
        self.definitiveChartId= 0

        if databaseRow:
            self.id = databaseRow[0]
            self.artistId = databaseRow[1]
            self.title = databaseRow[2]
            self.definitiveChartId = databaseRow[3]
            self.updateTime = databaseRow[4]


    def __str__(self):
        stringRep = "SongData { id=" + str(self.id) + ", "

        stringRep += "artistId=" + str(self.artistId) + ", "
        stringRep += "title=" + self.title + ", "
        stringRep += "definitiveChartId=" + str(self.definitiveChartId) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
