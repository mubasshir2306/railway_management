from psycopg2 import connect, Error
from dotenv import load_dotenv
from os import environ as env
import database
import random
import string
import datetime

load_dotenv()


def get_connection():
    connection = None

    try:
        connection = connect(
            host=env.get("HOST_NAME"),
            port=env.get("PORT_NAME"),
            user=env.get("USER_NAME"),
            password=env.get("PASSWORD"),
            database=env.get("DATABASE_NAME")
        )

    except Error as e:
        print(f"Error '{e}' occurred while attempting to connect to the database.")

    return connection


def check_userid(shouldnot: bool = False):
    while True:
        userid = input("Enter a UserID: ").lower()
        match = string.ascii_letters + string.digits + '_'
        if ' ' in userid:
            print("Please enter a UserID without any space(s)!")
        elif not all([x in match for x in userid]):
            print("UserID must only contain Alphabets, Numbers and Underscore.")
        elif len(userid) == 0:
            print("Please enter a valid UserID!")
        elif len(userid) < 6 or len(userid) > 20:
            print("Please enter a UserID with between 6 to 20 characters!")
        elif not userid[0].isalpha():
            print("UserID must start with a letter.")
        else:
            table = 'users'
            field = 'userid'
            exists = database.check_if_exists(table, field, userid)
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


def check_mobileno(userid: str = None, shouldnot: bool = False):
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
                table = 'users'
                field = 'mobileno'
                exists = database.check_if_exists(table, field, mobileno)
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


def check_name():
    while True:
        fullname = input("Enter your Full Name: ")
        match = string.ascii_letters + '.' + ' '
        if not all([x in match for x in fullname]):
            print("Please enter a Valid Name!")
        elif len(fullname) > 40:
            print("Name too long!")
        else:
            fullname = fullname.upper()
            return fullname


def check_age(passenger: bool = False):
    while True:
        try:
            age = int(input("Enter your age: "))
        except ValueError:
            print("Please Enter a Valid Age. ")
            continue
        if passenger:
            if age > 0 or age < 120:
                return age
            else:
                print("Enter a Valid Age between 0 and 120 Year!")
        else:
            if age < 18:
                print("You must at-least be 18 Years Old! ")
            elif age > 100:
                print("Maximum allowed age is 100 years!")
            else:
                return age


def check_sex():
    while True:
        sex = input("Enter your sex(M/F/OTH): ")
        if sex.upper() == 'M' or sex.upper() == 'F' or sex.upper() == 'OTH':
            sex = sex.upper()
            return sex
        else:
            print("Please enter one of the given options (M/F/OTH): ")


def check_train_number():
    while True:
        try:
            train_no = int(input("Enter the Train Number: "))
        except ValueError:
            print("Please enter a valid Train Number!")
            continue
        else:
            table = 'train_info'
            field = 'train_no'
            exists = database.check_if_exists(table, field, train_no)
            if exists:
                return train_no
            else:
                print("Please enter a valid Train Number!")


def check_if_station_code_exists(location: str):
    while True:
        code = input(f"Enter {location} Station Code: ").upper().strip()
        table = 'train_routes'
        field = 'station_code'
        exists = database.check_if_exists(table, field, code)
        if not exists:
            print("Enter a Valid Station Code!")
        else:
            return code


def check_station_code_with_train_no(train_no, location: str = None):
    while True:
        try:
            station_code = str(check_if_station_code_exists(location))
        except ValueError:
            print("Please enter a Valid Station Code!")
            continue
        else:
            table = 'train_routes'
            field = 'station_code'
            exists = database.check_if_exists(table, field, station_code.upper().strip(),
                                              and_where={'train_no': train_no})
            if exists:
                return station_code.upper()
            else:
                print(f"Station Code: {station_code.upper().strip()} is NOT a Stoppage for Train Number: {train_no}")


def generate_pnr():
    pnr = str(random.randint(100, 999)) + '-' + str(random.randint(1000000, 9999999))
    return pnr


def generate_ticket_no():
    n = 7
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
    return str(res)


def get_date():
    while True:
        try:
            date = input("Enter the Date of Journey(DD-MM-YYYY): ")
            date_journey = datetime.datetime.strptime(date, "%d-%m-%Y").date()
            return date_journey
        except ValueError:
            print("Please Enter the Correct Date!")


def get_class():
    print(
        "Please Enter The Class Name\n"
        "Press 1AC for First AC.\n"
        "Press 2AC for 2 Tier AC.\n"
        "Press 3AC for 3 Tier AC.\n"
        "Press SL for Sleeper.\n"
    )
    while True:
        class_name = input("Enter the Class: ")
        if class_name.upper().strip() == '1AC' or class_name.upper().strip() == '2AC' \
                or class_name.upper().strip() == '3AC' or class_name.upper().strip() == 'SL':
            class_name = class_name.upper().strip()
            return class_name
        else:
            print("Please Enter the Correct Class (1AC/2AC/3AC/SL): ")


def check_date(date):
    today = datetime.date.today()
    d1 = today.strftime("%d-%m-%Y")
    max_date = today + datetime.timedelta(days=90)
    d2 = max_date.strftime("%d-%m-%Y")

    while date < datetime.datetime.strptime(d1, "%d-%m-%Y").date() or \
            date > datetime.datetime.strptime(d2, "%d-%m-%Y").date():
        print(f"Please enter a Date Between {d1} And {d2}")
        date = input("Date(DD-MM-YYYY): ")
        date = datetime.datetime.strptime(date, "%d-%m-%Y")
        date = date.date()
        return


def get_num_pass():
    while True:
        try:
            num_pass = int(input("Enter the Number of Passengers: "))
        except ValueError:
            print("Enter a Valid Number!")
            continue
        else:
            if num_pass > 5:
                print("Maximum 5 Passengers are allowed in One Ticket!")
            elif num_pass <= 0:
                print("Please enter a number between 1 and 5.")
            else:
                return num_pass


def get_passenger_details(num):
    print(f"Enter Details of Passenger {num+1}: ")
    name = check_name()
    age = check_age(passenger=True)
    sex = check_sex()
    return name, age, sex


def check_pnr():
    while True:
        pnr = input("Enter the PNR Number of Your Booking: ")
        match = string.digits + '-'
        if not all([x in match for x in pnr]):
            print("Please enter a valid PNR Number!")
        elif len(pnr) != 11:
            print("Please enter a valid PNR Number!")
        elif pnr[3] != '-':
            print("Please enter a valid PNR Number!")
        else:
            spnr = ''
            und = ''
            for i in range(len(pnr)):
                if pnr[i] != '-':
                    spnr += pnr[i]
                else:
                    und += pnr[i]
            if len(spnr) != 10:
                print("Please enter a valid PNR Number!")
            elif und != '-':
                print("Please enter a valid PNR Number!")
            else:
                return pnr
