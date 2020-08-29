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
            sql_query_person = "INSERT INTO person (person_id, name, email_id, phone_no, aadhar_no) " \
                               "VALUES (%s, %s, %s, %s, %s)"
            values = (str(person_object.person_id),
                      person_object.name,
                      person_object.email_id,
                      person_object.phone_no,
                      person_object.person_id)
            person_status = self.connection.execute_query_with_values(sql_query_person, values)
        return person_status

    def create_booking(
            self,
            bookings_object,
    ):
        if not self.connection:
            return False
        else:
            sql_query = "INSERT INTO bookings (person_id, seat_id) VALUES (%s, %s)"
            values = (bookings_object.person_id, bookings_object.seat_id)
            sql_query_seat = f"UPDATE seats SET available = 0 WHERE seat_id = %s"
            seat_value = (int(bookings_object.seat_id), )
            book_status = self.connection.execute_query_with_values(
                sql_query=sql_query,
                values=values
            )
            seat_status = self.connection.execute_query_with_values(
                sql_query=sql_query_seat,
                values=seat_value
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
                        available=True if seat[2] == 1 else False,
                        flight_id=seat[1]
                    )
                )
            return {
                "count": len(seats),
                "seats": seat_objects
            }

    def get_bookings(
            self,
            person_id
    ):
        if not self.connection:
            return None
        else:
            booking_query = f"SELECT * FROM bookings WHERE person_id='{person_id}'"
            bookings = self.connection.execute_fetch_query(sql_query=booking_query)
            if bookings is None:
                logger.error("No seats available for the given flight id")
                return None
            bookin_details = []
            for booking in bookings:
                get_flight_query = f"SELECT * FROM flights WHERE " \
                                   f"flight_id=(SELECT flight_id FROM seats WHERE seat_id = {booking[1]})"
                flight = self.connection.execute_fetch_query(sql_query=get_flight_query)
                person_query = f"SELECT * FROM person WHERE aadhar_no='{booking[0]}'"
                person = self.connection.execute_fetch_query(sql_query=person_query)
                current_booking = {
                    "person_id": person[0][0],
                    "name": person[0][1],
                    "seat_id": booking[1],
                    "flight_id": flight[0][0],
                    "airlines": flight[0][1],
                    "source": flight[0][4],
                    "destination": flight[0][5],
                    "arrival": flight[0][2],
                    "departure": flight[0][3],
                }
                bookin_details.append(current_booking)
            return {
                "count": len(bookings),
                "bookings": bookin_details
            }
