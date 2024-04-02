import sqlite3
from sqlite3 import DatabaseError
from loguru import logger
from datetime import datetime

class Database:
    def __init__(self, db_file):
        """ create a database connection to a SQLite database """

        # Ensure db_file ends with .db extension
        if not db_file.endswith('.db'):
            db_file += '.db'
        logger.info(f"Initializing the database with the given name {db_file}")

        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except DatabaseError as e:
            logger.error(f"Couldn't initialize the database with the given name {db_file}")
            logger.error(e)
            raise DatabaseCantBeInitialized(e)

        if self.conn:
            logger.info(f"Database initialized with the given name {db_file}")

    def create_table(self, table_name, table_structure):
        """ create a table with the given name and structure in the database
        Make sure to properly format table_name before using this"""
        logger.info(f"Creating table {table_name} with structure {table_structure}")
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} ({table_structure})
                """)
                logger.info(f"Table {table_name} created successfully")
            except sqlite3.DatabaseError as e:
                print(e)
                raise DatabaseCantBeInitialized(e)

    def store_data(self, table_name, columns, data):
        """ store data in the database """
        if self.conn:
            try:
                logger.info(f"Storing data in the table {table_name} and columns {columns} and data {data}")
                cursor = self.conn.cursor()
                placeholders = ', '.join('?' * len(data))
                table_name = self.format_table_name(table_name)
                query = f"""
                    INSERT OR IGNORE INTO {table_name}({columns}) VALUES({placeholders})
                """
                logger.info(f"Query: {query}")
                cursor.execute(query, data)
                self.conn.commit()
            except DatabaseError as e:
                print(e)
                raise DatabaseCantBeInitialized(e)

    def fetch_data(self, table_name, sort_by: str = None):
        """Fetch data from the database, sorted by the specified column."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(f"""
                    SELECT * FROM {table_name} {"ORDER BY" + sort_by + "DESC" if not sort_by is None else ""}
                """)
                return cursor.fetchall()
            except DatabaseError as e:
                print(e)
                raise DatabaseCantBeInitialized(e)

    def fetch_all_tables(self):
        """Fetch data from all tables in the database."""
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                all_data = {}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT * FROM {table_name} ORDER BY date DESC")
                    all_data[table_name] = cursor.fetchall()

                return all_data
            except DatabaseError as e:
                print(e)
                raise DatabaseCantBeInitialized(e)

    @staticmethod
    def format_table_name(table_name: str) -> str:
        """Format the table name."""
        table_name = table_name.replace("-", "")
        if not table_name.startswith("date"):
            return "date" + table_name
        return table_name

    def fetch_and_sort_table_dates(self):
        # Fetch all table names
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Remove table names that don't start with "date"
        tables = [table for table in tables if table[0].startswith("date")]

        # Remove "date" prefix and sort
        dates = [table[0][4:] for table in tables]

        # Convert strings to datetime objects and sor
        sorted_dates = []
        for date in dates:
            try:
                sorted_dates.append(datetime.strptime(date, '%Y%m%d'))
            except ValueError:
                logger.error(f"Couldn't convert date {date} to datetime object")

        sorted_dates = sorted(sorted_dates)

        # Convert datetime objects back to strings
        sorted_dates = [date.strftime('%Y%m%d') for date in sorted_dates]
        logger.info(f"Sorted dates: {sorted_dates}")
        return sorted_dates


class DatabaseCantBeInitialized(Exception):
    pass
