import mysql.connector as connector
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class Connection:
    """
    A class for basic connections and query execution with
    mysql connector
    """

    def __init__(
            self,
            dbname,
            host,
            password,
            user
    ):
        """
        Constructor to initialize the db connection

        :param dbname: Database Name
        :param host: Host name
        :param password: Password
        :param user: Database Username
        """
        try:
            self._con = connector.connect(
                host=host,
                database=dbname,
                user=user,
                passwd=password
            )
            self.cursor = self._con.cursor()
        except connector.Error as e:
            logger.error(f'Error: {e}')
            self._con = None
            self._cursor = None
            self.cursor = None

    def execute_query(
            self,
            sql_query
    ):
        """
        Function to execute one query

        :param sql_query: The query to execute
        :return: true if successfull else false
        """
        if self._con:
            try:
                self._cursor.execute(sql_query)
                self._con.commit()
                return True
            except connector.Error as e:
                logger.error(f"Error: {e}")
                return False

    def execute_query_with_values(
            self,
            sql_query,
            values
    ):
        """
        Function to execute one insert into query with values

        :param sql_query: The query
        :param values: The values
        :return: True or false
        """
        if self._con:
            try:
                self._cursor.execute(sql_query, values)
                self._con.commit()
                return True
            except connector.Error as e:
                logger.error(f"Error: {e}")
                return False

    def execute_query_with_multiple_values(
            self,
            sql_query,
            values
    ):
        """
        Function to execute many insert into query with values

        :param sql_query: The query
        :param values: The values
        :return: True or false
        """
        if self._con:
            try:
                self._cursor.executemany(sql_query, values)
                self._con.commit()
                return True
            except connector.Error as e:
                logger.error(f"Error: {e}")
                return False

    def get_table_names(self):
        self._cursor.execute("SHOW TABLES")
        result_set = self.cursor.fetchall()
        list_tables = []
        for result in result_set:
            list_tables.append(result[0])
        return list_tables
