class ChartData:
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self, artist=None, title=None, key=None, chords=None, sections=None):
        self.artist = artist if artist is not None
        self.title = title if title is not None
        self.key = key if key is not None
        self.chords = chords if chords is not None
        self.sections = sections if sections is not None
