from .chartdata import ChartData

class MusicChartParser:
    """
    Parses data from a chord chart. Looks for information like title, key, chords, and structure.
    """
    def __init__(self):
        self._resetSongData()

    def _resetSongData(self):
        self.artist = None
        self.songTitle = None
        self.songSource = None
        self.chordList = []
        self.sectionList = []


    def _parseTitle(self, chartText):
        # Dummy data for now
        return "Dummy Data For The Win"


    def _parseKey(self, chartText):
        # Dummy data for now
        return "Cm"


    def _parseChords(self, chartText):
        chords = []

        # Dummy data for now
        chords.append("Cm")
        chords.append("Fm")
        chords.append("G")

        return chords


    def _parseSections(self, chartText):
        sections = []

        # Dummy data for now
        sections.append("Verse")
        sections.append("Chorus")
        sections.append("Verse")
        sections.append("Chorus")

        return sections


    def parseChart(self, chartText):
        chartData = ChartData()
        lines = chartText.splitlines()

        chartData.artist = self.artist
        chartData.title = self.songTitle
        chartData.source = self.songSource

        for line in lines:
            self.chordList.extend(self._parseChords(line))
            self.sectionList.extend(self._parseSections(line))

        chartData.chords = self.chordList
        chartData.sections = self.sectionList

        self._resetSongData()

        return chartData
