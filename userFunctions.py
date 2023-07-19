import database
from psycopg2 import Error
from tabulate import tabulate


def create_user():

    while True:
        field = 'userid'
        userid = input("Enter a UserID: ").lower()
        if len(userid) == 0:
            print("Please enter a valid UserID!")
        elif len(userid) > 20:
            print("Please enter a UserID with not more than 20 characters!")
        elif ' ' in userid:
            print("Please enter a UserID without any space(s)")
        else:
            exists = database.check_if_exists(field, userid)
            if exists:
                print("UserID already taken. Please enter a different UserID.")
            else:
                break

    while True:
        fullname = input("Enter your Full Name: ")
        if len(fullname) == 0:
            print("Please enter a valid Name!")
        elif len(fullname) > 40:
            print("Name too long!")
        else:
            fullname = fullname.upper()
            break

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
                if exists:
                    print("This Mobile Number already taken. Please enter a different Mobile Number.")
                else:
                    if len(str(mobileno)) == 10 and mobileno != 0000000000:
                        break
                    else:
                        print("Enter a valid Mobile Number")

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