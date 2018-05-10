import os
import os.path
import glob

import sqlite3 as sqlite

import pandas as pd

BASEDIR = os.path.join("..", "..")

PPMI_DATABASE_FILE = os.path.join(BASEDIR, "database", "ppmi.db")  

class SqliteCursor(object):
    """ 
        This is a thin wrapper class for the sqlite cursor. It takes care of
        opening and closing the connection and cursor.  
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite.connect(self.db_file)
        self.curs = self.conn.cursor()

    def __del__(self):
        if self.curs is not None:
            self.curs.close()
            self.curs = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute(self, *args, **kwargs):
        if self.curs is not None:
            return self.curs.execute(*args, **kwargs)
        else:
            raise ValueError("Cursor is not set")

    def cursor(self):
        return self.curs

    def connection(self):
        return self.conn

    @staticmethod
    def ppmi():
        """ Return a cursor to the ppmi sqlite database """
        return (SqliteCursor(PPMI_DATABASE_FILE))

def fetch_ppmi_csv_filenames():
    return glob.glob(os.path.join(BASEDIR, "data_docs", "*.csv"))

def fetch_raw_ppmi_data_file(filepath):
    return pandas.read_csv(filepath,
            low_memory=False,
            dtype={'PATNO':str})

def fetch_ppmi_data_file(filename, directory):
    """Read in the csv files from the data directory"""
    filepath = os.path.join(BASEDIR, directory, filename)
    return fetch_raw_ppmi_data_file(filepath)

