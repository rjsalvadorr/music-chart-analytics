from .basedata import BaseDataObject

class ChartCalculations(BaseDataObject):
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self, databaseRow=None):
        BaseDataObject.__init__(self)

        self.chartId= 0
        self.keys = []
        """ Keys in the piece (list of strings) """
        self.keyChords = []
        """
        Generic chords in the piece.
        Rep'd as a list of strings, with each string showing chords in each key.
        This list is parallel to the `keys` list above.
        """

        # When returning a ChartCalculations object from the database, this can be initialized.
        self.chartData = None

        if databaseRow:
            self.id = databaseRow[0]
            self.chartId = databaseRow[1]
            self.setKeysFromString(databaseRow[2])
            self.setKeyChordsFromString(databaseRow[4])
            self.updateTime = databaseRow[5]

    def setKeysFromString(self, keyStr):
        blacklistValues = ['[]', 'None']
        if keyStr and keyStr not in blacklistValues and keyStr is not None:
            if self.delim2 in keyStr:
                convertedList = self._convertStringToList(keyStr)
                self.keys = convertedList
            else:
                keyList = []
                keyList.append(keyStr)
                self.keys = keyList

    def getKeysString(self):
        if not self.keys:
            return ''
        else:
            return self._convertListToString(self.keys)

    def setKeyChordsFromString(self, keyChordsStr):
        convertedList = self._convertStringToTwoDimensionList(keyChordsStr)
        self.keyChords = convertedList

        if not self.keyChords:
            self.keyChords = []

    def getKeyChordsString(self):
        if not self.keyChords:
            return ''
        else:
            return self._convertTwoDimensionListToString(self.keyChords)

    def __str__(self):
        stringRep = "ChartCalculations { id=" + str(self.id) + ", "

        stringRep += "chartId=" + str(self.chartId) + ", "
        stringRep += "keys=" + str(self.keys) + ", "
        stringRep += "keyChords=" + str(self.keyChords) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
