from mchartanalyzer.chartanalyzer import ChartAnalyzer

cAnalyzer = ChartAnalyzer()


print("\n===== TESTING KEY STRING CONVERSION =====")
keyStrings = ["Bb Major", "D# Minor", "G major", "Eb Minor"]

for keyString in keyStrings:
    result = cAnalyzer._convertKeyTextToMusic21(keyString)
    print(keyString + " -> " + result)


print("\n===== TESTING CHORD SYMBOL CONVERSION =====")
chordSymbolList1 = ["C", "G", "F", "G", "C", "Am", "Dm", "G"]
chordSymbolList2 = ["Dm", "A", "Dm", "C", "F", "C", "Dm", "A"]
chordSymbolList3 = ["Bbm", "F", "Bbm", "Ab", "Db", "Ab", "Bbm", "F"]

keyList = ["C Major", "D Minor", "Bb Minor"]

genChordList1 = cAnalyzer._convertChordListToGeneral(chordSymbolList1, keyList[0])
genChordList2 = cAnalyzer._convertChordListToGeneral(chordSymbolList2, keyList[1])
genChordList3 = cAnalyzer._convertChordListToGeneral(chordSymbolList3, keyList[2])

print(keyList[0])
for index, chordSym in enumerate(chordSymbolList1):
    print(chordSym + " -> " + genChordList1[index])

print(keyList[1])
for index, chordSym in enumerate(chordSymbolList2):
    print(chordSym + " -> " + genChordList2[index])

print(keyList[2])
for index, chordSym in enumerate(chordSymbolList3):
    print(chordSym + " -> " + genChordList3[index])

print("\n===== GETTING MOST COMMON CHORDS =====")
chordList = "F,F9,C,F9,C,G,F,F9,C,F9,C,G,F,G,Em7,F,G,F,F9,C,F9,C,G,F,F9,C,F9,C,G,F,G,Em7,F,G,B,E,A,D,G,F,G,Em7,F,G".split(",")
res = cAnalyzer._getMostCommonChords(chordList)
print(res)
