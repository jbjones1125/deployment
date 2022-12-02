from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Database:
    def __init__(self, name):
        '''
        Creates an instance of the database class, only one instance will be
        open at any time
        :param name: string name of the database
        :return: an instance of the Database class
        '''
        self.db = name

    def connect(self):
        '''
        Creates a database connection
        :return: None
        '''
        pass

    def disconnect(self):
        '''
        Removes database connection (if required)
        :return: None
        '''
        pass

    def getTable(self, table):
        '''
        Retrieves a table from the database
        :param table: string table name
        :return: list of rows from the result of the query
        '''
        pass

    def addRow(self, table, values):
        '''
        Add a new row of info to a table in the database
        :param table: String table name
        :param values: list of values
        :return: None
        '''
        pass

    def delRow(self, table, primaryKey):
        '''
        Deletes a row from a table in the database
        :param table: string table name
        :param primaryKey: primary key of the table
        :return: None
        '''
        pass