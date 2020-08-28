import logging
from database.initialize import Initialize
from database.connection import Connection
from model.fbs_model import Flights, Seats

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class DfbsDao:
    def __init__(
            self,
            dbname,
            user,
            password,
            host
    ):
        initialize = Initialize(dbname, host, password, user)
        self.connection = None
        if not initialize.check_data():
            if initialize.create():
                self.connection = Connection(
                    dbname=dbname,
                    host=host,
                    password=password,
                    user=user
                )
            else:
                logger.error("There was some error while creating the DB")
        else:
            self.connection = Connection(
                dbname=dbname,
                host=host,
                password=password,
                user=user
            )
        if self.connection is None:
            raise ValueError("Unable to initialize database")

    def create_person(
            self,
            person_object,
    ):
        if not self.connection:
            return False
        else:
            sql_query_person = "INSERT INTO person (name,email_id,phone_no,aadhar_no) VALUES (%s,%s,%s,%s)"
            values = (person_object.name,
                      person_object.email_id,
                      person_object.phone_no,
                      person_object.aadhar_no)
            person_status = self.connection.execute_query_with_values(sql_query_person, values)
        return person_status

    def create_booking(
            self,
            bookings_object,
            person_object
    ):
        if not self.connection:
            return False
        else:
            sql_query = "INSERT INTO bookings (aadhar_no, seat_id) VALUES (%s, %s)"
            values = (bookings_object.person_id, bookings_object.seat_id)
            sql_query_seat = f"UPDATE seats SET available = False " \
                             f"WHERE seat_id = '{bookings_object.seat_id}'"
            book_status = self.connection.execute_query_with_values(
                sql_query=sql_query,
                values=values
            )
            seat_status = self.connection.execute_query(
                sql_query=sql_query_seat
            )
            if book_status and seat_status:
                return True
            else:
                return False

    def get_available_flights(
            self,
            source,
            destination
    ):
        if not self.connection:
            return None
        else:
            sql_query = f"SELECT * FROM flights WHERE SOURCE='{source}' AND DESTINATION = '{destination}'"
            resultset = self.connection.execute_fetch_query(sql_query)
            if resultset is not None:
                flight_objects = []
                for result in resultset:
                    current_flight_object = Flights(
                        flight_id=result[0],
                        name=result[1],
                        arrival=result[2],
                        departure=result[3],
                        source=result[4],
                        destination=result[5]
                    )
                    flight_objects.append(current_flight_object)
                return flight_objects

            else:
                logger.error("Error fetching details from the database")

    def get_available_seats(
            self,
            flight_id
    ):
        if not self.connection:
            return None
        else:
            seats_query = f"SELECT * FROM seats WHERE flight_id='{flight_id}'"
            seats = self.connection.execute_fetch_query(sql_query=seats_query)
            if seats is None:
                logger.error("No seats available for the given flight id")
                return None
            seat_objects = []
            for seat in seats:
                seat_objects.append(
                    Seats(
                        seat_id=seat[0],
                        available=True if seat[1] == "YES" else False,
                        flight_id=seat[1]
                    )
                )
            return {
                "count": len(seats),
                "seats": seat_objects
            }
