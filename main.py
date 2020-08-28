# This is the driver for the whole application which allows simple flight
# checking and booking functionalities

from __future__ import print_function, unicode_literals
import logging
import sys
from pyfiglet import Figlet
from dao.dfbs_dao import DfbsDao
from PyInquirer import prompt
from examples import custom_style_2

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s'
)

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
    print(answers.get("dbname"))

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
                    'message': 'Enter the source city in short form (ex: DEL)'
                },
            ]
            answers_travel = prompt(travel_questions, style=custom_style_2)
            dao_object.get_available_flights(
                source=answers_travel.get("source"),
                destination=answers_travel.get("destination")
            )
        else:
            print(answers.get("choice") + "\n")
