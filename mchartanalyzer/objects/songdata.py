from .basedata import BaseDataObject

class SongData(BaseDataObject):
    """
    Class encapsulating basic information about a song.
    """

    def __init__(self):
        BaseDataObject.__init__(self)

        self.artistId = 0
        self.title = ""


    def __str__(self):
        stringRep = "SongData { id=" + str(self.id) + ", "
        
        stringRep += "artistId=" + str(self.artistId) + ", "
        stringRep += "title=" + self.title + ", "

        stringRep += "updateTime=" + self.updateTime + " }"

        return stringRep
