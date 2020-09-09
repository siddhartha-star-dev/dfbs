# This is the driver for the whole application which provides simple flight
# checking and booking functionalities

from __future__ import print_function, unicode_literals
import regex
from prettytable import PrettyTable
import logging
import sys
from pyfiglet import Figlet
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
from examples import custom_style_2
from dao.dfbs_dao import DfbsDao
from model.fbs_model import Person, Bookings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
)


class SeatNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[0-9]*$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter only numeric value',
                cursor_position=len(document.text))
        if int(document.text) < 1 or int(document.text) > 10:
            raise ValidationError(
                message='Please enter a number between 1 and 10',
                cursor_position=len(document.text))


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[0-9]{10}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter only numeric value with strictly 10 digits',
                cursor_position=len(document.text))


class AdhaarNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[0-9]{12}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid Adhaar number',
                cursor_position=len(document.text))


class EmailValidator(Validator):
    def validate(self, document):
        ok = regex.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid email address',
                cursor_position=len(document.text))


# The driver programme
if __name__ == '__main__':
    print("Started the application, initializing database\n")
    questions = [
        {
            'type': 'input',
            'name': 'host',
            'message': 'Enter the host name for the database'
        },
        {
            'type': 'input',
            'name': 'dbname',
            'message': 'Enter the database name for the database'
        },
        {
            'type': 'input',
            'name': 'user_name',
            'message': 'Enter the username for the database'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter the password for the database'
        }
    ]

    answers = prompt(questions, style=custom_style_2)

    dbname = answers.get("dbname")
    user_name = answers.get("user_name")
    host = answers.get("host")
    password = answers.get("password")

    print(
        "Attempting to initialize connection to the database,"
        " in case the required tables do not exist, they will be created\n"
    )
    try:
        dao_object = DfbsDao(
            user=user_name,
            host=host,
            dbname=dbname,
            password=password
        )
        print("Successfully connected to the database\n")
        welcome_message = Figlet(font='slant')
        print(welcome_message.renderText("Welcome to FBS!!"))
    except ValueError:
        print("Error with the details provided please restart the application to continue\n")
        sys.exit("Problem with the database details provided")

    while True:
        menu_questions = [
            {
                "type": "list",
                "name": "choice",
                "message": "Select the operation you want to perform",
                "choices": [
                    "Make a booking",
                    "View your bookings",
                    "Search for flights",
                    "Exit"
                ]
            }
        ]
        answers = prompt(menu_questions, style=custom_style_2)
        choice = answers.get("choice")

        if choice == "Exit":
            break

        elif choice == "Search for flights":
            travel_questions = [
                {
                    'type': 'input',
                    'name': 'source',
                    'message': 'Enter the source city in short form (ex: DEL)'
                },
                {
                    'type': 'input',
                    'name': 'destination',
                    'message': 'Enter the destination city in short form (ex: DEL)'
                },
            ]
            print("\nAll the flights in the schedule run daily\n")
            answers_travel = prompt(travel_questions, style=custom_style_2)
            available_flights = dao_object.get_available_flights(
                source=answers_travel.get("source"),
                destination=answers_travel.get("destination")
            )
            flights_output = PrettyTable()
            flights_output.field_names = [
                "Flight ID",
                "Airlines",
                "Source",
                "Destination",
                "Arrival Time",
                "Departure Time",
            ]
            for flight_object in available_flights:
                flights_output.add_row([
                    flight_object.flight_id,
                    flight_object.name,
                    flight_object.source,
                    flight_object.destination,
                    flight_object.arrival,
                    flight_object.departure
                ])
            print("\nAvailable flights\n")
            print(flights_output)
            print("\n")

        elif choice == "View your bookings":
            booking_questions = [
                {
                    'type': 'input',
                    'name': 'person_id',
                    'message': 'Enter the adhaar number',
                    "validate": AdhaarNumberValidator
                },
            ]
            answers_booking = prompt(booking_questions, style=custom_style_2)
            bookings = dao_object.get_bookings(person_id=answers_booking.get("person_id"))
            bookings_table = PrettyTable()
            bookings_table.field_names = [
                "Adhaar Number",
                "Name",
                "Seat Id",
                "Flight Id",
                "Airlines",
                "Source",
                "Destination",
                "Arrival",
                "Departure",
            ]
            print(f"\nThere are {bookings['count']} bookings for the provided Aadhar Number \n")
            for booking in bookings["bookings"]:
                bookings_table.add_row([
                    booking["person_id"],
                    booking["name"],
                    booking["seat_id"],
                    booking["flight_id"],
                    booking["airlines"],
                    booking["source"],
                    booking["destination"],
                    booking["arrival"],
                    booking["departure"]
                ])
            print(bookings_table)

        elif choice == "Make a booking":
            print("\nYou need to have the flight id ready in order to make a booking.\n"
                  "In case you do not know the flight id yet, please search for flights instead\n"
                  "To exit the menu, press Ctrl + C\n")
            travel_questions = [
                {
                    'type': 'input',
                    'name': 'flight_id',
                    'message': 'Enter the flight ID you want to book seats in'
                },
                {
                    'type': 'input',
                    'name': 'num_seats',
                    'message': 'Enter the number of seats you wish to book',
                    'validate': SeatNumberValidator
                },

            ]
            answers_travel = prompt(travel_questions, style=custom_style_2)
            available_seats = dao_object.get_available_seats(flight_id=answers_travel.get("flight_id"))
            seat_selection_questions = [
                {
                    'type': 'checkbox',
                    'message': 'select seats',
                    'name': 'seats_selected',
                    'choices': []
                }
            ]

            if available_seats["count"] == 0:
                print("\nSorry currently all seats in the flight are booked please try again\n")

            elif available_seats["count"] < int(answers_travel.get("num_seats")):
                print("\nSorry there are not enough seats as per the requirement please try again\n")

            else:
                for available_seat in available_seats["seats"]:
                    if available_seat.available:
                        seat_selection_questions[0]["choices"].append(
                            {
                                "name": str(available_seat.seat_id)
                            }
                        )

                if len(seat_selection_questions[0]["choices"]) == 0:
                    print("\nSorry currently all seats in the flight are booked please try again\n")

                else:
                    selected_seats = prompt(seat_selection_questions, style=custom_style_2)

                    if len(selected_seats) != int(answers_travel.get("num_seats")):
                        print("\nYou need to select exactly the number of seats you want to book\n")

                    else:
                        person_questions = [
                            {
                                "type": "input",
                                "name": "name",
                                "message": "Enter name"
                            },
                            {
                                "type": "input",
                                "name": "email",
                                "message": "Enter email address",
                                "validate": EmailValidator
                            },
                            {
                                "type": "input",
                                "name": "phone_number",
                                "message": "Enter contact number",
                                "validate": PhoneNumberValidator
                            },
                            {
                                "type": "input",
                                "name": "adhaar_number",
                                "message": "Enter Adhaar Number",
                                "validate": AdhaarNumberValidator
                            }
                        ]

                        for i in range(1, int(answers_travel.get("num_seats"))+1):
                            print(f"Please Enter details for passenger : {i}")
                            current_seat = available_seats["seats"][i-1].seat_id
                            answer_passenger = prompt(person_questions, style=custom_style_2)
                            current_passenger = Person(
                                name=answer_passenger.get("name"),
                                email_id=answer_passenger.get("email"),
                                phone_no=int(answer_passenger.get("phone_number")),
                                person_id=int(answer_passenger.get("adhaar_number"))
                            )
                            person_status = dao_object.create_person(
                                person_object=current_passenger
                            )

                            if not person_status:
                                print("\nSorry we encountered some error try again later\n")
                                break
                            current_booking = Bookings(
                                person_id=current_passenger.person_id,
                                seat_id=current_seat
                            )
                            bookingstatus = dao_object.create_booking(
                                bookings_object=current_booking
                            )

                            if not bookingstatus:
                                print("\nSorry we encountered some error try again later\n")
                                break

                            else:
                                print(f"\nSuccessfully booked seat for : {current_passenger.name}\n")

        else:
            print(answers.get("choice") + "\n")
