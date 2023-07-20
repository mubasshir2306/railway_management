from psycopg2 import connect, Error
from dotenv import load_dotenv
from os import environ as env
import database

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
            field = 'userid'
            table = 'users'
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
                field = 'mobileno'
                table = 'users'
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