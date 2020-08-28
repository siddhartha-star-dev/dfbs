# This file defines the various models representing the
# entities in the system


class Seats:
    def __init__(
            self,
            seat_id,
            available,
            flight_id,
    ):
        self.seat_id = seat_id
        self.available = available
        self.flight_id = flight_id


class Flights:

    def __init__(
            self,
            flight_id,
            name,
            arrival,
            departure,
            source,
            destination,
    ):
        self.flight_id = flight_id
        self.name = name
        self.arrival = arrival
        self.departure = departure
        self.source = source
        self.destination = destination


class Person:

    def __init__(
            self,
            name,
            email_id,
            phone_no,
            person_id
    ):
        self.name = name
        self.email_id = email_id
        self.phone_no = phone_no
        self.person_id = person_id


class Bookings:

    def __init__(
            self,
            person_id,
            seat_id,
    ):
        self.person_id = person_id
        self.seat_id = seat_id
