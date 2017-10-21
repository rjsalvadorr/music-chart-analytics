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
            self.key = databaseRow[2]
            self.keyAnalysisCertainty = databaseRow[3]
            self.chordsGeneral = self._convertStringToList(databaseRow[4])
            self.updateTime = databaseRow[7]

    def setChordListFromString(self, chordListStr):
        convertedList = self._convertStringToList(chordListStr)
        self.chordsGeneral = convertedList

    def getChordListString(self):
        return self._convertListToString(self.chordsGeneral)

    def __str__(self):
        stringRep = "ChartCalculations { id=" + str(self.id) + ", "

        stringRep += "chartId=" + str(self.chartId) + ", "
        stringRep += "key=" + self.key + ", "
        stringRep += "keyAnalysisCertainty=" + self.keyAnalysisCertainty + ", "
        stringRep += "chordsGeneral=[" + self.getChordListString() + "], "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
