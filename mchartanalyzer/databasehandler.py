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
        return self.dbConnection.cursor()

    def _commit(self):
        self.dbConnection.commit()

    def _close(self):
        self.dbConnection.close()

    def _commitAndClose(self):
        self.dbConnection.commit()
        self.dbConnection.close()


    def saveChartData(self, chartData):
        c = self._connect()

        # Sample SQLite snippet:
        # INSERT INTO CHARTS('id','song_id','source_url','chords_specific','sections','is_new','update_time') VALUES (NULL,NULL,NULL,NULL,NULL,NULL,NULL);

        # A) Inserts an ID with a specific value in a second column
        try:
            c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
                format(tn=table_name, idf=id_column, cn=column_name))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        # B) Tries to insert an ID (if it does not exist yet)
        # with a specific value in a second column
        c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
                format(tn=table_name, idf=id_column, cn=column_name))

        # C) Updates the newly inserted or pre-existing entry
        c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
                format(tn=table_name, cn=column_name, idf=id_column))

        self._commitAndClose()


    def saveArtistData(self, chartData):
        c = self._connect()

        # Sample SQLite snippet:
        # INSERT INTO ARTISTS('name','source_names','source_urls','update_time') VALUES ('test_script','sources','urls','times');

        self._commitAndClose()


    def saveChartCalculationData(self, chartData):
        c = self._connect()

        self._close()


    def saveArtistCalculationData(self, chartData):
        c = self._connect()

        self._close()


    def _getSongByTitle(self, title):
        c = self._connect()

        # SELECT * FROM SONGS WHERE TITLE = 'WHATEVER'

        self._close()


    def getNewChartRecords(self):
        c = self._connect()

        # 1) Contents of all columns for row that match a certain value in 1 column
        c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.\
                format(tn=table_name, cn=column_2))
        all_rows = c.fetchall()

        self._close()
