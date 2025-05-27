"""
db main module to manage SQLite database

Classes:

    Db
"""

from typing import Any
import sqlite3
from ..utils.status import LogLevel, Logger


class Db:
    """
    This class provides a simple interface to the different functionalities
    of the Python SQLite module, to easily and quickly perform the various
    operations on databases:

    Attributes
    -----------
    status: dict[int,str]
        A convenient container to holds infos about the state of the object,
        it's a kind of rudimentary logger
    last_intsertid: in
        holds the id of he last inserted entry in the database
    database: str
        the full path to the database to use
    connection: sqlite3.Connection
        the connection object to the database
    cursor: sqlite3.Cursor | None
        the cursor on the datanase

    Methods
    -------
    connect
        Takes no parameter, return thhe `connection` attribute
    disconnect
        this method close the connectio; called by the destructor
    db_read
        return records from the databases; essentially do `SELECT` queries
    db_write
        all other types of queries done on the database:
            - insert
            - update
            - delete
    """

    def __init__(self, db_path: str) -> None:
        """
        Initialization of the Db object

            Parameters:
                status (dict[int,str]) contains the state of the object
                last_inserted_id (int) holds the id of he last inserted entry in the database
                db_path (str): contains the full path to the database
                connection (sqlite3.Connection): a connection object to the database
                cursor (sqlite3.Cursor): a cursor pointer in hte database
        """
        # 0: everything nothing to log, 1: error, 2: warning, 3: info, 4: success
        self.logger: Logger = Logger()
        self.last_inserted_id: int = 0
        self.database: str = db_path
        self.connection: sqlite3.Connection = self.db_connect()
        self.cursor: sqlite3.Cursor | None = None
        if self.logger.get_level() == LogLevel.OK:
            self.cursor = self.connection.cursor()

    def __del__(self):
        """Safely closing the connection when going out of scope"""
        self.db_close()

    def db_connect(self) -> sqlite3.Connection | None:
        """
        Operates connection to the database, and initialize the self.connecton attribute

            Returns:
                bool True on succes, False on failure to connect to the daatabase and update the status attriv=bute
        """
        con: sqlite3.Connection | None = None
        try:
            con = sqlite3.connect(self.database)
        except (sqlite3.OperationalError, sqlite3.Error) as ex:
            self.logger.set_log(LogLevel.ERROR, ex)

        return con

    def db_close(self) -> None:
        """
        This method is responsible for closing the connection to the database
        """
        try:
            if self.logger:
                self.connection.close()
        except (sqlite3.OperationalError, sqlite3.Error) as ex:
            self.logger.set_log(LogLevel.ERROR, ex)

    def db_read(self, query: str, params: tuple[Any], single_row: bool = True) -> Any:
        """
        Execute a select query on the database

            Parameters:
                query (str) the query to execute
                params (tuple[any]) the value of the query to escape
                single_row (bool) whether to query one or multiple rows

            Returns:
                The result of the query
        """
        result: Any = None

        try:
            result = self.cursor.execute(query, params)
            if single_row:
                result.fetchone()
            else:
                result.fetchall()
        except (sqlite3.OperationalError, sqlite3.Error) as ex:
            self.logger.set_log(LogLevel.ERROR, ex)
            result = None

        return result

    def db_write(
        self, query: str, data: dict[str, Any], insert: bool, single_row: bool = True
    ) -> None:
        """
        Execute queries other than select (insert, delete, update)

            Parameters:
                query (str) the query to execute
                data (dict[str,Any]) the value of the query to escape
                insert (bool) n case of insertion the method update the last_inserted_id attribute
                single_row (bool) whether to affect one or multiple rows

            Returns:
                None
        """
        try:
            if single_row:
                self.cursor.execute(query, data)
                if insert:
                    self.last_inserted_id = self.cursor.lastrowid
            else:
                self.executemany(query, data)

        except (sqlite3.OperationalError, sqlite3.Error) as ex:
            self.logger.set_log(LogLevel.ERROR, ex)

        self.connection.commit()
