# from musicchartparser.chartdata import ChartData
# WHY DOES THIS HAVE TO BE AN ABSOLUTE PATH?
# I don't see why a module just can't import fellow modules in the same package

from .chartdata import ChartData

class MusicChartParser:
    """
    Parses data from a chord chart. Looks for information like title, key, chords, and structure.
    """
    def __init__(self):
        self._resetSongData()


    def setArtistName(self, artistName):
        """
        Sets the artist name for a chart.
        """
        self.artistName = artistName


    def setSongName(self, songName):
        """
        Sets the song name for a chart.
        """
        self.songName = songName


    def _resetSongData(self):
        self.artistName = None
        self.songName = None
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

        chartData.artist = self.artistName
        chartData.title = self.songName

        for line in lines:
            self.chordList.extend(self._parseChords(line))
            self.sectionList.extend(self._parseSections(line))

        chartData.chords = self.chordList
        chartData.sections = self.sectionList

        self._resetSongData()

        return chartData
