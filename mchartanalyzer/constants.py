import os

MOST_COMMON_CHORDS_LIMIT = 5
TEST_MODE_SONG_LIMIT = 3
URL_SCRAPE_COOLDOWN_DAYS = 30

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(MODULE_DIR)
DATETIME_FORMAT = "%Y-%m-%d-%H:%M:%S"

DATA_OUTPUT_DIRNAME = "mchartanalyzer-data"
DATA_OUTPUT_DIR = os.path.join(PROJECT_DIR, DATA_OUTPUT_DIRNAME)

DATABASE_FILENAME = "mchartdatabase.db"
DATABASE_FILE_PATH = os.path.join(DATA_OUTPUT_DIR, DATABASE_FILENAME)
