import pprint
from mchartanalyzer.chartanalyzer import ChartAnalyzer

pPrinter = pprint.PrettyPrinter(indent=2, width=120)
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

print("\n===== GETTING MOST COMMON CHORD PROGRESSIONS =====")
testProg = 'Am,F,G,Am,F,G,Am,F,G,Am,G,Am7,Am,G,Am7,Am,G,Am7,D,F,Am,F,G,Am,F,G,Am,G,Am7,Am,G,Am7,Am,G,Am7,F,G,A6,G,Bbm,C#,Bbm,C#,Bbm,C#,Bbm,C#,Bbm,G#,Bbm7,Bbm,G#,Bbm7,Bbm,G#,Bbm7,Cm7,F#,Bbm,G#,Bbm7,Bbm,G#,Bbm7,Bbm,G#,Bbm7,Bbm,G#,Bbm7,Bbm,G#,Bbm7'.split(',')
progs = cAnalyzer._getChordProgressions(testProg)
pPrinter.pprint(progs)

giantString = 'i,i,bVII,III,iv,i,iv,III,bVII,i,bVII,III,iv,i,iv,III,bVII,i,III,i,iv,III,bVII,i,III,i,iv,III,bVII,i,i,III,i,iv,III,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,i,III,i,i,iv,III,bVII,i,III,i,iv,III,bVII,i,III,iv,III,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,v,bVII,v,IV,i,bVI,V,i,bVI,V,i,bVI,V,i,bVI,V,V,V,V,i,i,III,i,i,iv,III,bVII,i,III,i,iv,III,bVII,i,III,iv,III,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVII,i,bVI,V,i,bVI,V,i,bVI,V,i,bVI,V,V,V,V,V,V,V,V'
testProg = giantString.split(',')
progs = cAnalyzer._getChordProgressions(testProg)
pPrinter.pprint(progs)
