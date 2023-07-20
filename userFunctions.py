import database
from psycopg2 import Error
import datetime
from trainRelatedQueries import find_all_trains, show_fares, get_station_code
from utils import check_mobileno, check_userid, check_name, check_age, check_sex


def create_user():

    userid = check_userid()

    fullname = check_name()

    mobileno = check_mobileno()

    age = check_age()

    sex = check_sex()

    try:
        database.create_user(userid, fullname, mobileno, age, sex)
        print("\nUser created successfully\n")
    except Error:
        print(f"\nAn error occurred, Please try again later. \n")


def book_tickets():

    current_date = datetime.date.today()
    max_date = current_date + datetime.timedelta(days=60)

    print(
        "\nSome Important Information Regarding Ticket Bookings:\n"
        "- You must be a Registered User.\n"
        "- A Registered User can Book Tickets for a Maximum of 5 Different Journeys.\n"
        "- A Ticket can be Booked 2 Months before the Actual Trip.\n"
        "- Please make sure to know Train Number, Starting Station Code and Destination "
        "Station Code before proceeding to Bookings.\n"
        "\nFollowing options may help you:"
    )

    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\nPress 1 to Check Trains.\n"
            "Press 2 to Check Fares.\n"
            "Press 3 to know Station Codes.\n"
            "Press X to continue to booking."
        )

        n = input("Enter your choice: ")

        if n == '1':
            find_all_trains()
        if n == '2':
            show_fares()
        if n == '3':
            get_station_code()

    userid = check_userid(shouldnot=True)
    mobileno = check_mobileno(userid=userid, shouldnot=True)

    print("\nBooking Started...")

