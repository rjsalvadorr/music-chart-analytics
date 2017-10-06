

class Utils:

    def convertToMusic21ChordSymbol(text):
        """
        Converts regular chord symbols into ones that music21 understands.
        The main difference: the flat accidental is "-" on music21, not "b".
        For example, this method would convert "Bbm7" to "B-m7"
        """
        formattedChordSymbol = text.replace("b", "-")
        # Specific replacements below were added after certain music21 errors.
        # TODO - find a better way to avoid these issues!
        formattedChordSymbol = formattedChordSymbol.replace("-5", "b5")
        formattedChordSymbol = formattedChordSymbol.replace("-9", "b9")
        formattedChordSymbol = formattedChordSymbol.replace("maj", "")
        formattedChordSymbol = formattedChordSymbol.replace("Maj", "")
        formattedChordSymbol = formattedChordSymbol.replace("Maj7", "M7")
        formattedChordSymbol = formattedChordSymbol.replace("7sus4", "sus4")

        return formattedChordSymbol
