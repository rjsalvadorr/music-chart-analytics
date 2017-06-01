from chartdata import ChartData

class MusicChartParser:
    """
    Parses data from a chord chart. Looks for information like title, key, chords, and structure.
    """
    def __init__(self):
        self.artistName = None
        self.songName = None


    def setArtistName(self, artistName):
        """
        Sets the artist name for a chart.
        Meant to be used in cases where the song name isn't in the chart itself.
        """
        self.artistName = artistName


    def setSongName(self, songName):
        """
        Sets the song name for a chart.
        Meant to be used in cases where the song name isn't in the chart itself.
        """
        self.songName = songName


    def _resetSongData(self):
        self.artistName = None
        self.songName = None


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

        if self.artistName and not self.artistName.isspace():
            chartData.artist = self.artistName

        if self.songName and not self.songName.isspace():
            chartData.title = self.songName

        self._resetSongData()

        chartData.chords = self._parseChords(chartText)
        chartData.sections = self._parseSections(chartText)

        return chartData
