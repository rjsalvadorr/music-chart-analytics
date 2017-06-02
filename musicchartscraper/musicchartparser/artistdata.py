
class ArtistData:
    """
    Class encapsulating all the desired data from the chord charts, after thorough analysis.
    """
    def __init__(self):
        # The properties listed below are good candidates for persistence and presentation
        self.artistName = ""
        self.sourceNames = ""
        self.sourceUrls = ""
        self.analysisTimestamp = None

        self.numSongs = 0
        self.numMajorKeys = 0
        self.numMinorKeys = 0

        self.numChordsSpecific = 0
        self.numChordsGeneral = 0

    def calculate(self):
        return 0

    def addChartData(self, chartData):
        self.chartDataList.append(chartData)
