from .basedata import BaseDataObject

class ChartCalculations(BaseDataObject):
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self):
        BaseDataObject.__init__(self)

        self.chartId= 0
        self.key = ""
        self.keyAnalysisCertainty = ""
        self.chordsGeneral = []
        self.numChords = 0


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
