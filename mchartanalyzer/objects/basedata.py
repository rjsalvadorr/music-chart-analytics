
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
        return listString.split(self.delim2)
