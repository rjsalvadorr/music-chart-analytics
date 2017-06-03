import os
import sqlite3

from . import constants

class DatabaseHandler:
    """
    Class responsible for handling database operations.
    """

    def __init__(self, testMode=None):
        self.dbConnection = None

    def _connect(self):
        self.dbConnection = sqlite3.connect(constants.DATABASE_FILE_PATH)

    def _commit(self):
        self.dbConnection.commit()

    def _close(self):
        self.dbConnection.close()

    def _commitAndClose(self):
        self.dbConnection.commit()
        self.dbConnection.close()

    def saveChartData(self, chartData):
        return 0

    def saveArtistData(self, chartData):
        return 0

    def saveChartCalculationData(self, chartData):
        return 0

    def saveArtistCalculationData(self, chartData):
        return 0

    def getNewChartRecords(self):
        return 0
