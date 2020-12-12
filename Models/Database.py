import sqlite3
from datetime import datetime
import json
import pandas as pd
class Database(): 

    def __init__(self, name):
        self.name = name
        self.error = ''
        self.open = False

        try:
            self.connection = sqlite3.connect('{}.db'.format(name))
            self.cursor = self.connection.cursor()
            self.open = True
            print(type(self.cursor))
        except sqlite3.Error as error:
            self._handleError(error)


    def open(self):
        try:
            self.connection = sqlite3.connect('{}.db'.format(name))
            self.open = True
            print("The Sqlite connection is open")


        except sqlite3.Error as error:
            self._handleError(error)


    def close(self):
        if (self.connection):
                self.connection.close()
                self.open = False
                print("The Sqlite connection is closed")


    def createCurrencyTable(self, currency):
        """
            This method create a database with the name of currency and the default 
            set of parameters of this currency
        """
        try:
            sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS """ + currency +"""( 
                                        date TEXT NOT NULL PRIMARY KEY,
                                        value REAL NOT NULL
                                        );"""
            self.cursor.execute(sqlite_create_table_query)
            self.connection.commit()
            print("SQLite table created")

        except sqlite3.Error as error:
            self._handleError(error)


    def insertCurrency(self, nameTable, currElems):
        try:
            sqlite_insert_query = """INSERT INTO """ + nameTable + """(date, value) 
                                VALUES (?, ?);"""
            self.cursor.execute(sqlite_insert_query, currElems)
            self.connection.commit()
        except sqlite3.Error as error:
            self._handleError(error)

    def saveJSON(self, data, curr): 
        self.createCurrencyTable("USD")

        for year in data["rates"].keys():
            print(year + ': ' + str(data["rates"][year][curr]))
            self.insertCurrency(curr, ( year, str(data["rates"][year][curr])))
 
    def saveDataframe(self, data):
        data.to_sql('Forecast', self.connection, if_exists='replace', index = False)

    def createBackup(self, nameOfCopy):
        try:
            #copy into this DB
            backup = Database("backupOf" + self.name + datetime.now().strftime("%m_%Y_%H"))
            with backup:
                self.connection.backup(backup, pages=3, progress=_progress)
            print("backup successful")

        except sqlite3.Error as error:
            self._handleError(error)

        finally:
            if(backup):
                backup.close()

    def readSqliteTable(self, tableName):
        """
            Read in the database the infos we are looking for in function of the 
        """
        try:
            print("Connected to SQLite")
            df = pd.read_sql_query("SELECT * from {}".format(tableName), self.connection)
            return df
        except sqlite3.Error as error:
            self._handleError(error)    


    def insertElementsTest(self):
        try:
            print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO """ + self.name + """
                                (id, name, email, joining_date, salary) 
                                VALUES (4, 'Jos', 'jos@gmail.com', '2019-01-14', 9500);"""
            self.cursor.execute(sqlite_insert_query)

            sql_update_query = """Update """ + self.name + """ set salary = 10000 where id = 4"""
            self.cursor.execute(sql_update_query)

            sql_delete_query = """DELETE from """ + self.name +""" where id = 4"""
            self.cursor.execute(sql_delete_query)
            self.connection.commit()

        except sqlite3.Error as error:
            self._handleError(error) 

    def _progress(self, status, remaining, total):
        print(f'Copied {total-remaining} of {total} pages...')

    def _handleError(self, error):
        self.error = error
        self._printError()

    def _printError(self):
        print("Eror in database : ", self.error)


    def __str__(self):
        return f"{self.name}"

    def __del__(self):
        if (self.open): 
            self.close()