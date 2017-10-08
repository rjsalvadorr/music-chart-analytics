import collections
import re

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
    formattedChordSymbol = formattedChordSymbol.replace("maj7", "M7")
    formattedChordSymbol = formattedChordSymbol.replace("Maj7", "M7")
    formattedChordSymbol = formattedChordSymbol.replace("maj9", "M9")
    formattedChordSymbol = formattedChordSymbol.replace("Maj9", "M9")
    formattedChordSymbol = formattedChordSymbol.replace("7sus4", "sus4")

    return formattedChordSymbol

def mergeDictionaries(primaryDict, secondaryDict):
    """
    Given two dictionaries, this merges the second into the first and returns the combined dictionary.
    """
    for dictKey in secondaryDict:
        if dictKey in primaryDict:
            primaryDict[dictKey] = primaryDict[dictKey] + secondaryDict[dictKey]
        else:
            primaryDict[dictKey] = secondaryDict[dictKey]

    return primaryDict

def sortAndTrimDict(rawDict, limit):
    """
    Given a dictionary and a limit, sorts the dictionary and trims it to the right number of entries.
    """
    newDict = collections.OrderedDict()
    sortedDict = sorted(rawDict, key=rawDict.get, reverse=True)

    ctr = 0
    for sortedDictKeys in sortedDict:
        ctr += 1
        newDict[sortedDictKeys] = rawDict[sortedDictKeys]
        if ctr >= limit:
            break

    return newDict

def substituteRomanChords(inChord):
    """
    Substitutes certain odd chord spellings with ones the system reads more easily
    """
    outChord = inChord.replace('75#3', '7')
    outChord = outChord.replace('ob753', 'o7')
    return outChord

def convertRomanScaleDegree(inText):
    """
    Converts scale degree text like '-VII' to 'bVII'.
    Also changes chords like 'vi7' to 'vi'
    """
    outText = inText.replace('-', 'b')

    return outText
