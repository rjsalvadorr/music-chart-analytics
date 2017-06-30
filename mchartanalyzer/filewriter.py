import os
import shutil
import traceback
from datetime import datetime

import yaml

from . import constants

class FileWriter:

    def __init__(self, testMode=None, yamlMode=None):
        self.testMode = True if testMode else False

        # Create output directory if it doesn't exist
        try:
            os.makedirs(constants.DATA_OUTPUT_DIR)
        except OSError:
            if not os.path.isdir(constants.DATA_OUTPUT_DIR):
                raise

        self.newFile()

    def newFile(self):
        """
        Starts a new log file.
        """
        self.startTime = datetime.now()

        if self.testMode:
            self.filename = "log-test.txt"
        else:
            self.filename = "log-" + self.startTime.strftime("%Y%m%d-%H%M%S") + ".txt"

        self.logPath = os.path.join(constants.DATA_OUTPUT_DIR, self.filename)
        self.log("LOG STARTED AT " + self.startTime.strftime(constants.DATETIME_FORMAT))
        self.log("==================================\n")

    def log(self, text):
        try:
            with open(self.logPath, 'a') as outFile:
                outFile.write(text)
                outFile.write("\n")
        except IOError as exc:
            print("ERROR! Unable to copy file. " + repr(exc))
        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

    def _formatArtistName(self, artistName):
        formattedName = artistName.lower().replace(' ', '-')
        return formattedName

    def writeArtistCalculations(self, artistCalcs):
        artistNameFormatted = self._formatArtistName(artistCalcs.artistData.name)
        timestamp =  datetime.now().strftime("%Y%m%d-%H%M%S")
        calcsFilename = "mChartAnalytics-" + artistNameFormatted + "-" + timestamp + ".yaml"
        calcsFilePath = os.path.join(constants.DATA_OUTPUT_DIR, calcsFilename)

        try:
            stream = open(calcsFilePath, 'w')
            yaml.dump(artistCalcs, stream)
            print("Data written to\n" + calcsFilePath + "\n")
        except Exception as exc:
            print("Error encountered while writing to YAML file: " + repr(exc))
            print(traceback.format_exc())
