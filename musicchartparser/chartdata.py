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

    def __str__(self):
        stringRep = "SONG: " + self.title.upper() + "\n"
        stringRep += "ARTIST: " + self.artist + "\n\n"

        stringRep += "KEY: " + self.key + "\n\n"

        stringRep += "CHORDS\n"
        for chord in chords:
            stringRep += chord + " "
        stringRep += "\n\n"

        stringRep += "SECTIONS\n"
        for section in sections:
            stringRep += section + " "
        stringRep += "\n"

        return stringRep
