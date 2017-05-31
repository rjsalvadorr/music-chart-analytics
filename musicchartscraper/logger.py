import os
import shutil
import traceback
from datetime import datetime

class Logger:
    def __init__(self):
        self.moduleDir = os.path.dirname(os.path.realpath(__file__))
        self.projectDir = os.path.dirname(self.moduleDir)
        self.outputDir = os.path.join(self.projectDir, "mchartanalyzer-output")

        # Create output directory if it doesn't exist
        try:
            os.makedirs(self.outputDir)
        except OSError:
            if not os.path.isdir(self.outputDir):
                raise

        self.newFile()


    def newFile(self):
        """
        Starts a new log file.
        """
        self.startTime = datetime.now()
        self.filename = "log-" + self.startTime.strftime("%Y%m%d-%H%M%S") + ".txt"
        self.logPath = os.path.join(self.outputDir, self.filename)

        self.log("LOG STARTED AT " + self.startTime.strftime("%Y-%m-%d %H:%M:%S"))
        self.log("==================================")


    def log(self, text):
        try:
            with open(self.logPath, 'a') as outFile:
                outFile.write(text)
                outFile.write("\n")
        except IOError as exc:
            print("ERROR! Unable to copy file. " + repr(exc))
        except Exception as exc:
            print("Unexpected error: " + repr(exc))
            print(traceback.format_exc())
