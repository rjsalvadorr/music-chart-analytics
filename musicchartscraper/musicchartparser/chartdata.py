
class ChartData:
    """
    Encapsulates data extracted from a chord chart.
    """

    def __init__(self):
        self.artist = None
        self.title = None
        self.source = None

        self.key = None
        self.chords = None
        self.sections = None

        self.keyAnalysisCertainty = None

    def __str__(self):
        stringRep = "SONG: " + self.title.upper() + "\n"
        stringRep += "ARTIST: " + self.artist + "\n"
        stringRep += "SOURCE: " + self.source + "\n\n"

        if self.key and not self.key.isspace():
            stringRep += "KEY: " + self.key + "\n"
            stringRep += "KEY ANALYSIS CERTAINTY: " + self.keyAnalysisCertainty + "\n\n"

        if self.chords:
            stringRep += "CHORDS\n"
            for chord in self.chords:
                stringRep += chord + " "
            stringRep += "\n\n"

        if self.sections:
            stringRep += "SECTIONS\n"
            for section in self.sections:
                stringRep += section + " "
            stringRep += "\n"

        return stringRep
