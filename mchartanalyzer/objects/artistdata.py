from .basedata import BaseDataObject

class ArtistData(BaseDataObject):
    """
    Class encapsulating basic information about an artist/musician.
    """

    def __init__(self):
        BaseDataObject.__init__(self)

        self.artistName = ""
        self.sourceNames = []
        self.sourceUrls = []


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

        stringRep += "artistName=" + self.artistName + ", "
        stringRep += "sourceNames=" + self.getSourceNamesAsString() + ", "
        stringRep += "sourceUrls=" + self.getSourceUrlsAsString() + ", "
        
        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
