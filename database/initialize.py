# Firstly check if database and tables exist if not then create

from database.connection import Connection

TABLE_FILE = 'table_file.txt'
DATA_SEATS = 'data_seats.txt'
DATA_FLIGHTS = 'data_flights.txt'
TABLE_NAMES = [
    'bookings',
    'flights',
    'person',
    'seats'
]


class Initialize:
    def __init__(
            self,
            dbname,
            host,
            password,
            user
    ):
        self.connection = Connection(
            dbname=dbname,
            host=host,
            password=password,
            user=user
        )

    def check_data(
            self,
            table_names=TABLE_NAMES
    ):
        if not self.connection.cursor:
            return False
        else:
            present_tables = self.connection.get_table_names()
            for table_name in table_names:
                if table_name not in present_tables:
                    return False
        return True

    def create(
            self,
            table_file=TABLE_FILE,
            data_flights=DATA_FLIGHTS,
            data_seats=DATA_SEATS
    ):
        if not self.connection.cursor:
            return False
        else:
            with open(table_file, 'r') as tables:
                lines = tables.readlines()
                for command in lines:
                    self.connection.execute_query(sql_query=command)
            with open(data_flights, 'r') as data:
                lines = data.readlines()
                for command in lines:
                    self.connection.execute_query(sql_query=command)
            with open(data_seats, 'r') as data:
                lines = data.readlines()
                for command in lines:
                    self.connection.execute_query(sql_query=command)
            return True
