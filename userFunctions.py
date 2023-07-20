import database
from psycopg2 import Error
import datetime
from trainRelatedQueries import find_all_trains, show_fares, get_station_code
from tabulate import tabulate


def check_userid(shouldnot: bool = False):
    while True:
        userid = input("Enter a UserID: ").lower()
        if len(userid) == 0:
            print("Please enter a valid UserID!")
        elif len(userid) > 20:
            print("Please enter a UserID with not more than 20 characters!")
        elif ' ' in userid:
            print("Please enter a UserID without any space(s)")
        else:
            field = 'userid'
            exists = database.check_if_exists(field, userid)
            if not shouldnot:
                if exists:
                    print("UserID already taken. Please enter a different UserID.")
                else:
                    return userid
            else:
                if exists:
                    return userid
                else:
                    print("This UserID does not exists. Please check your UserID and try again.")


def check_mobileno(userid:str = None, shouldnot:bool = False):
    while True:
        try:
            mobileno = int(input("Enter your Mobile Number: "))
        except ValueError:
            print("Please Enter a Valid Mobile Number!")
            continue
        else:
            if len(str(mobileno)) > 10 or len(str(mobileno)) < 10:
                print("Please Enter a Valid 10 Digit Mobile Number!")
            else:
                field = 'mobileno'
                exists = database.check_if_exists(field, mobileno)
                if not shouldnot:
                    if exists:
                        print("This Mobile Number already taken. Please enter a different Mobile Number.")
                    else:
                        if len(str(mobileno)) == 10 and mobileno != 0000000000:
                            return mobileno
                        else:
                            print("Enter a valid Mobile Number")
                else:
                    if exists:
                        if exists[0][1] == userid:
                            return mobileno
                        else:
                            print(f"This Mobile Number does not match with the "
                                  f"Mobile Number registered with UserID: {userid}\n"
                                  "Please check the Mobile Number and try again!")
                    else:
                        print(f"This Mobile Number does not match with the "
                                  f"Mobile Number registered with UserID: {userid}\n"
                                  "Please check the Mobile Number and try again!")


def create_user():

    userid = check_userid()

    while True:
        fullname = input("Enter your Full Name: ")
        if len(fullname) == 0:
            print("Please enter a valid Name!")
        elif len(fullname) > 40:
            print("Name too long!")
        else:
            fullname = fullname.upper()
            break

    mobileno = check_mobileno()

    while True:
        try:
            age = int(input("Enter your age: "))
        except ValueError:
            print("Please Enter a Valid Age. ")
            continue
        else:
            if age < 18:
                print("You must be at-least 18 years old! ")
            elif age > 100:
                print("Maximum allowed age is 100 years!")
            else:
                break

    while True:
        sex = input("Enter your sex(M/F/OTH): ")
        if sex.upper() == 'M' or sex.upper() == 'F' or sex.upper() == 'OTH':
            sex = sex.upper()
            break
        else:
            print("Please enter one of the given options: M/F/OTH ")

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

