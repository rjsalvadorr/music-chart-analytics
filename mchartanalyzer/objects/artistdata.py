from .basedata import BaseDataObject

class ArtistData(BaseDataObject):
    """
    Class encapsulating basic information about an artist/musician.
    """

    def __init__(self, databaseRow=None):
        BaseDataObject.__init__(self)

        self.name = ""
        self.sourceNames = []
        self.sourceUrls = []

        if databaseRow:
            self.id = databaseRow[0]
            self.name = databaseRow[1]
            self.sourceNames = self._convertStringToList(databaseRow[2])
            self.sourceUrls = self._convertStringToList(databaseRow[3])
            self.updateTime = databaseRow[4]


    def setSourceNamesFromString(self, sourceNamesStr):
        convertedList = self._convertStringToList(sourceNamesStr)
        self.sourceNames = convertedList


    def setSourceUrlsFromString(self, sourceUrlsStr):
        convertedList = self._convertStringToList(sourceUrlsStr)
        self.sourceUrls = convertedList


    def getSourceNamesAsString(self):
        return self._convertListToString(self.sourceNames)


    def getSourceUrlsAsString(self):
        return self._convertListToString(self.sourceUrls)


    def __str__(self):
        stringRep = "ArtistData { id=" + str(self.id) + ", "

        stringRep += "artistName=" + self.name + ", "
        stringRep += "sourceNames=[" + self.getSourceNamesAsString() + "], "
        stringRep += "sourceUrls=[" + self.getSourceUrlsAsString() + "], "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
