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
            self.keys = databaseRow[2]
            self.keyChords = self._convertStringToList(databaseRow[3])
            self.updateTime = databaseRow[4]

    def setKeysFromString(self, keyStr):
        convertedList = self._convertStringToList(keyStr)
        self.keys = convertedList

    def getKeysString(self):
        return self._convertListToString(self.keys)

    def setKeyChordsFromString(self, keyChordsStr):
        convertedList = self._convertStringToList(keyChordsStr)
        self.keyChords = convertedList

    def getKeyChordsString(self):
        return self._convertListToString(self.keyChords)

    def __str__(self):
        stringRep = "ChartCalculations { id=" + str(self.id) + ", "

        stringRep += "chartId=" + str(self.chartId) + ", "
        stringRep += "keys=" + self.keys + ", "
        stringRep += "keyChords=" + self.keyChords + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
