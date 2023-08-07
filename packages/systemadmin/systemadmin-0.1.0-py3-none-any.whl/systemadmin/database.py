import sqlite3
import pandas

from sqlite3 import Cursor


class Database:

    def __init__(self, database: str, table: str) -> None:
        """
        :param database: database name
        :param table: table name
        :rtype: None
        """
        self.database = database
        self.table = table
        self.connection = sqlite3.connect(database)

    def create(self, table) -> None:
        # On ne peut pas mettre le nom de la table comme paramètre !
        # https://stackoverflow.com/questions/228912/sqlite-parameter-substitution-problem
        self.connection.execute(f"CREATE TABLE {table} (Score INT)")

    def drop(self, table) -> None:
        # On ne peut pas mettre le nom de la table comme paramètre !
        # https://stackoverflow.com/questions/228912/sqlite-parameter-substitution-problem
        self.connection.execute(f"DROP TABLE IF EXISTS {table}")

    def select(self, table) -> Cursor:
        # On ne peut pas mettre le nom de la table comme paramètre !
        # https://stackoverflow.com/questions/228912/sqlite-parameter-substitution-problem
        return self.connection.execute(f"SELECT * FROM {table}")

    def insert_int(self, table, int_value) -> None:
        self.connection.execute(f"INSERT INTO {table} (Score) VALUES ({int_value})")

    def insert_df(self, table: str, df: pandas.DataFrame) -> None:
        df.to_sql(table, con=self.connection, if_exists='append')


    @staticmethod
    def print_select(cursor) -> None:
        rows = cursor.fetchall()
        for row in rows:
            print(row)
