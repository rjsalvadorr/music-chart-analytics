import os
import sqlite3
import traceback
from datetime import datetime

from . import constants

class DatabaseHandler:
    """
    Class responsible for handling database operations.
    """

    def __init__(self, testMode=None):
        self.dbConnection = None
        self.dbOpened = False

    def _connect(self):
        if not self.dbOpened:
            self.dbConnection = sqlite3.connect(constants.DATABASE_FILE_PATH)
            self.dbOpened = True
        return self.dbConnection.cursor()

    def _commit(self):
        self.dbConnection.commit()

    def _close(self):
        if self.dbOpened:
            self.dbConnection.close()
            self.dbOpened = False

    def _commitAndClose(self):
        if self.dbOpened:
            self.dbConnection.commit()
            self.dbConnection.close()
            self.dbOpened = False


    def saveArtistData(self, artistData):
        """
        Saves artist data to the database.
        """

        # Sample SQLite snippet: INSERT INTO ARTISTS('name','source_names','source_urls','update_time') VALUES ('test_script','sources','urls','times');
        insertStmt = "INSERT INTO ARTISTS('name','source_names','source_urls','update_time') VALUES (\'{artistName}\', \'{sourceNames}\', \'{sourceUrls}\', \'{updateTime}\')"
        updateStmt = "UPDATE ARTISTS SET 'source_names' = \'{sourceNames}\', 'source_urls' = \'{sourceUrls}\', 'update_time' = \'{updateTime}\' WHERE name=(\'{artistName}\')"

        try:
            c = self._connect()
            existingArtist = self.getArtistByName(artistData.name, keepConnectionOpen=True)
            timestampStr = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            if existingArtist:
                # Artist with this name already exists. Update it.
                finalQuery = updateStmt.format(artistName=artistData.name, sourceNames=artistData.getSourceNamesAsString(), sourceUrls=artistData.getSourceUrlsAsString(), updateTime=timestampStr)
                print("Running query: " + finalQuery)
                c.execute(finalQuery)
            else:
                # Artist does not exist yet. Insert new record.
                finalQuery = insertStmt.format(artistName=artistData.name, sourceNames=artistData.getSourceNamesAsString(), sourceUrls=artistData.getSourceUrlsAsString(), updateTime=timestampStr)
                print("Running query: " + finalQuery)
                c.execute(finalQuery)

        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column!')

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._commitAndClose()


    def saveSongData(self, artistData, songData):
        """
        Saves song data to the database.
        If a song with the same name exists in the database, nothing happens.
        """

        # Sample SQLite snippet: INSERT INTO ARTISTS('name','source_names','source_urls','update_time') VALUES ('test_script','sources','urls','times');
        insertStmt = "INSERT INTO SONGS('artist_id','title','update_time') VALUES ({artistId}, \'{songTitle}\', \'{updateTime}\')"

        try:
            c = self._connect()
            existingArtist = self.getArtistByName(artistData.name, keepConnectionOpen=True)
            existingSong = self.getSongByTitle(songData.title, keepConnectionOpen=True)
            timestampStr = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            if not existingSong:
                # Song does not exist yet. Insert new record.
                finalQuery = insertStmt.format(artistId=artistData.id, songTitle=songData.title, updateTime=timestampStr)
                print("Running query: " + finalQuery)
                c.execute(finalQuery)

        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column!')

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._commitAndClose()


    def saveChartData(self, songData, chartData):
        """
        Saves chart data to the database.
        If a chart with the same URL exists, the existing record is updated with the newer chords and sections.
        """

        # Sample SQLite snippet: INSERT INTO CHARTS('id','song_id','source_url','chords_specific','sections','is_new','update_time') VALUES (NULL,NULL,NULL,NULL,NULL,NULL,NULL);
        insertStmt = "INSERT INTO CHARTS('song_id','source_url','chords_specific','sections','is_new','update_time') VALUES ({songId}, {url}, {chordList}, {sectionList}, 1, {updateTime})"
        updateStmt = "UPDATE CHARTS SET 'chords_specific' = {chordList}, 'sections' = {sectionList}, 'is_new' = 1, 'update_time' = {updateTime} WHERE song_id={songId} AND source_url={url}"

        try:
            c = self._connect()
            existingChart = self.getChartByUrl(chartData.source, keepConnectionOpen=True)
            existingSong = self.getSongByTitle(chartData.title, keepConnectionOpen=True)
            timestampStr = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            if existingChart:
                # Chart from this source already exists. Update it.
                c.execute(updateStmt.format(songId=existingSong.id, url=chartData.source, chordList=chartData.getChordListString(), sectionList=chartData.getSectionListString(), updateTime=timestampStr))
            else:
                # Chart does not exist yet. Insert new record.
                c.execute(insertStmt.format(songId=existingSong.id, url=chartData.source, chordList=chartData.getChordListString(), sectionList=chartData.getSectionListString(), updateTime=timestampStr))

        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column!')

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._commitAndClose()


    def saveChartCalculationData(self, chartData):
        """
        Saves chart calculations to the database.
        """
        try:
            c = self._connect()

            # ...

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._commitAndClose()


    def saveArtistCalculationData(self, chartData):
        """
        Saves artist calculations to the database.
        """
        try:
            c = self._connect()

            # ...

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._commitAndClose()


    def getArtistByName(self, title, keepConnectionOpen):
        """
        Retrieves an artist with the given name.
        Returns "None" if a record isn't found.
        """
        try:
            c = self._connect()

            # SELECT * FROM CHARTS WHERE 'source_url' = 'http://whatevs.ca'

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            if not keepConnectionOpen:
                self._close()

        return 0


    def getSongByTitle(self, title, keepConnectionOpen):
        """
        Retrieves a song with the given title.
        Returns "None" if a record isn't found.
        """
        try:
            c = self._connect()

            # SELECT * FROM SONGS WHERE title = 'WHATEVER'

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            if not keepConnectionOpen:
                self._close()

        return 0


    def getChartByUrl(self, title, keepConnectionOpen):
        """
        Retrieves a chart with the given source URL.
        Returns "None" if a record isn't found.
        """
        try:
            c = self._connect()

            # SELECT * FROM CHARTS WHERE 'source_url' = 'http://whatevs.ca'

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            if not keepConnectionOpen:
                self._close()

        return 0


    def getNewChartRecords(self):
        """
        Retrieves charts which haven't been analyzed yet.
        Returns "None" if there are no new charts.
        """
        try:
            c = self._connect()

            # 1) Contents of all columns for row that match a certain value in 1 column
            c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.format(tn=table_name, cn=column_2))
            all_rows = c.fetchall()

        except Exception as exc:
            print("UNEXPECTED ERROR: " + repr(exc))
            print(traceback.format_exc())

        finally:
            self._close()
