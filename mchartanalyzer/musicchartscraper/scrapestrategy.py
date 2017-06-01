from abc import ABC, abstractmethod

class ScrapeStrategy(ABC):
    """
    Abstract base class, representing a strategy for navigating a particular website.
    One concrete subclass should be implemented for each website we're interested in.
    """

    # TODO - add a "getSongTitle()" method here

    @abstractmethod
    def _formatArtistName(self, artistName):
        pass

    @abstractmethod
    def _getArtistUrl(self, artistName):
        pass

    @abstractmethod
    def getSongUrls(self):
        pass
