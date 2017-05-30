from abc import ABCMeta

class ScrapeStrategy:
    """
    Abstract base class, representing a strategy for navigating a particular website.
    One concrete subclass should be implemented for each website we're interested in.
    """
    __metaclass__ = ABCMeta

    # TODO - figure out what each Strategy obj will need
    """
    - main URL root
    - format for main artist URL
    - format for song URLs
    """

    @abstractmethod
    def getArtistUrl(self):
        pass

    @abstractmethod
    def getSongUrl(self):
        pass
