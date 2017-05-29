from abc import ABCMeta

class ScrapeStrategy:
    """
    Base class, representing a strategy for navigating a particular website.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def getArtistUrl(self):
        pass

    @abstractmethod
    def getSongUrl(self):
        pass
