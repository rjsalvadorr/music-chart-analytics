from mchartanalyzer.objects.basedata import BaseDataObject

baseDataObj = BaseDataObject()

testDict = {}
testDict['DeRozan'] = 10
testDict['Lowry'] = 7
testDict['Joseph'] = 6
testDict['Tucker'] = 2
testDict['Ibaka'] = 9

print("\nTest Dictionary:\n" + str(testDict) + "\n")

testDictString = baseDataObj._convertDictToString(testDict)
print("String Rep:\n" + testDictString + "\n")

testDict2 = baseDataObj._convertStringToDict(testDictString)
print("Test Dictionary Again:\n" + str(testDict2) + "\n")
