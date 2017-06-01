
class ChartData:
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self):
        self.artist = None
        self.title = None
        self.key = None
        self.chords = None
        self.sections = None
        self.source = None

    def __str__(self):
        stringRep = "SONG: " + self.title.upper() + "\n"
        stringRep += "ARTIST: " + self.artist + "\n"
        stringRep += "SOURCE: " + self.source + "\n\n"

        if self.key and not self.key.isspace():
            stringRep += "KEY: " + self.key + "\n\n"

        stringRep += "CHORDS\n"
        for chord in self.chords:
            stringRep += chord + " "
        stringRep += "\n\n"

        stringRep += "SECTIONS\n"
        for section in self.sections:
            stringRep += section + " "
        stringRep += "\n"

        return stringRep
