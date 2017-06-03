import os
import shutil
import traceback
from datetime import datetime

from . import constants

class Logger:

    def __init__(self, testMode=None):

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
        self.log("LOG STARTED AT " + self.startTime.strftime("%Y-%m-%d %H:%M:%S"))
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
