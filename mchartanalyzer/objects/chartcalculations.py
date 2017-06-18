from .basedata import BaseDataObject

class ChartCalculations(BaseDataObject):
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self, databaseRow=None):
        BaseDataObject.__init__(self)

        self.chartId= 0
        self.key = ""
        self.keyAnalysisCertainty = ""
        self.chordsGeneral = []
        self.numChords = 0 # TODO - remove?
        self.numSections = 0 # TODO - remove?

        # When returning a ChartCalculations object from the database, this can be initialized.
        self.chartData = None

        if databaseRow:
            self.id = databaseRow[0]
            self.chartId = databaseRow[1]
            self.key = databaseRow[2]
            self.keyAnalysisCertainty = databaseRow[3]
            self.chordsGeneral = self._convertStringToList(databaseRow[4])
            self.numChords = databaseRow[5]
            self.numSections = databaseRow[6]
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
        stringRep += "numChords=" + str(self.numChords) + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
