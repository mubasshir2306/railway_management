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
        if len(userid) == 0:
            print("Please enter a valid UserID!")
        elif len(userid) > 20:
            print("Please enter a UserID with not more than 20 characters!")
        elif ' ' in userid:
            print("Please enter a UserID without any space(s)")
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
        if len(fullname) == 0:
            print("Please enter a valid Name!")
        elif len(fullname) > 40:
            print("Name too long!")
        else:
            fullname = fullname.upper()
            return fullname


def check_age():
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
                return age


def check_sex():
    while True:
        sex = input("Enter your sex(M/F/OTH): ")
        if sex.upper() == 'M' or sex.upper() == 'F' or sex.upper() == 'OTH':
            sex = sex.upper()
            return sex
        else:
            print("Please enter one of the given options: M/F/OTH ")


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
            print("Enter a valid Station Code!")
        else:
            return code


def check_station_code_with_train_no(train_no, location: str = None):
    while True:
        try:
            station_code = str(check_if_station_code_exists(location))
        except ValueError:
            print("Please enter a valid Station Code!")
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
            date = input("Enter the Date of Journey(YYYY-MM-DD): ")
            date_journey = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            return date_journey
        except ValueError:
            print("Please Enter the Correct Date!")


