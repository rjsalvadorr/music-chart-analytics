
class BaseDataObject:
    """
    Represents base class of the various data objects.
    """

    def __init__(self):
        self.id = 0
        self.updateTime = ""

        self.delim1 = ";"
        self.delim2 = ","

    def _convertListToString(self, myList):
        """
        Returns a string representation of a list
        """
        return self.delim2.join(myList)

    def _convertStringToList(self, listString):
        """
        Returns a list from its string representation
        """
        if listString:
            return listString.split(self.delim2)
        else:
            return []

    def _convertTwoDimensionListToString(self, myList):
        """
        Returns a string representation of a two-dimensional list
        """
        flatList = []
        for innerList in myList:
            listStr = self.delim2.join(innerList)
            flatList.append(listStr)
        return self.delim1.join(flatList)

    def _convertStringToTwoDimensionList(self, listString):
        """
        Returns a list from its string representation
        """
        if listString:
            newList = []
            stageList = listString.split(self.delim1)
            for innerListString in stageList:
                newList.append(innerListString.split(self.delim2))

            return newList
        else:
            return []

    def _convertStringToDict(self, dictString):
        """
        Returns a dict from its string representation
        """
        myDict = {}

        entries = dictString.split(self.delim1)

        for entry in entries:
            pair = entry.split(self.delim2)
            myDict[pair[0]] = pair[1]

        return myDict

    def _convertDictToString(self, myDict):
        """
        Returns a string representation of a simple dictionary
        """
        dictString = ''

        for myKey, myVal in myDict.items():
            dictString += str(myKey) + self.delim2 + str(myVal) + self.delim1

        return dictString[:-1]
