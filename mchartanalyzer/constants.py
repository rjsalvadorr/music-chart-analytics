import os

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(MODULE_DIR)

DATA_OUTPUT_DIRNAME = "mchartanalyzer-data"
DATA_OUTPUT_DIR = os.path.join(PROJECT_DIR, DATA_OUTPUT_DIRNAME)

DATABASE_FILENAME = "mchartdatabase.db"
DATABASE_FILE_PATH = os.path.join(DATA_OUTPUT_DIR, DATABASE_FILENAME)