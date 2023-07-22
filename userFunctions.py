import database
from psycopg2 import Error
from tabulate import tabulate
import datetime
import time
from trainRelatedQueries import find_all_trains, show_fares, get_station_code, check_if_route_exists
from utils import check_mobileno, check_userid, check_name, check_age, check_sex, check_train_number, \
    check_station_code_with_train_no, generate_pnr, generate_ticket_no, get_date, get_class, check_date, \
    get_num_pass, get_passenger_details, check_pnr


def create_user():
    userid = check_userid()
    fullname = check_name()
    mobileno = check_mobileno()
    age = check_age()
    sex = check_sex()

    try:
        database.create_user(userid, fullname, mobileno, age, sex)
        print("\nUser Created Successfully!\n")
    except Error:
        print(f"\nAn error occurred, Please try again later. \n")


def book_tickets():
    print(
        "\nSome Important Information Regarding Ticket Bookings:\n"
        "- You Must be a Registered User.\n"
        "- A Registered User can Book Tickets for a Maximum of 5 Different Journeys.\n"
        "- A Ticket can be Booked 3 Months before the Actual Trip.\n"
        "- A Maximum of 5 Passengers can be Booked in One Ticket.\n"
        "- Please make sure to know Train Number, Boarding Station Code and Destination "
        "Station Code before proceeding to Bookings.\n"
        "\nFollowing Options might help you:"
    )

    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\nPress 1 to Check Trains.\n"
            "Press 2 to Check Fares.\n"
            "Press 3 to know Station Codes.\n"
            "Press X ==> CONTINUE TO BOOKING."
        )
        n = input("Enter Your Choice: ")
        if n == '1':
            find_all_trains()
        if n == '2':
            show_fares()
        if n == '3':
            get_station_code()

    userid = check_userid(shouldnot=True)
    if database.check_max_bookings(userid) < 5:
        check_mobileno(userid=userid, shouldnot=True)
        train_no = check_train_number()
        start_station_code = check_station_code_with_train_no(train_no, 'Boarding')
        end_station_code = check_station_code_with_train_no(train_no, 'Destination')
        exists = check_if_route_exists(train_no, start_station_code, end_station_code)
        if not exists:
            print("Returning to Main Menu...")
            return
        else:
            departure_time = database.get_time(train_no, start_station_code, 'departure_time')
            arrival_time = database.get_time(train_no, end_station_code, 'arrival_time')
            ticket_no = generate_ticket_no()
            pnr = generate_pnr()
            date = get_date()
            check_date(date)
            class_name = get_class()
            num_pass = get_num_pass()
            for num in range(num_pass):
                passenger = get_passenger_details(num)
                status = 'CNF'
                database.book_ticket(ticket_no, userid, pnr, train_no, start_station_code, end_station_code, date,
                                     departure_time, arrival_time, passenger[0], passenger[1], passenger[2], class_name,
                                     status)
                print(f"Passenger {num + 1} Added Successfully!")

            print(f"\nTicket Booked!")
            print(
                f"Your PNR Number is: {pnr}\n"
                "Please Note Down Your PNR Number as it is Used to Check Bookings and Cancel Bookings."
            )
    else:
        print("Cannot Proceed with Booking. Maximum Booking Limit Reached!")
        return


def show_booking():
    userid = check_userid(shouldnot=True)
    check_mobileno(userid=userid, shouldnot=True)
    pnr = check_pnr()
    exists = database.check_if_exists('bookings', 'pnr', pnr, and_where={'userid': userid})
    if not exists:
        print(f"UserID: '{userid}' Does Not Have a Booking With PNR Number: '{pnr}'")
        return
    else:
        res = database.show_booking(userid, pnr)
        if not res:
            print("No Bookings Found!")
        else:
            date = res[0][6]
            d1 = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            d2 = d1.strftime("%d-%m-%Y")
            print('\n'
                  f"Ticket Number:   {res[0][0]}\n"
                  f"PNR Number:      {res[0][2]}\n"
                  f"Train Number:    {res[0][3]}\n"
                  f"Train Name:      {res[0][14]}\n"
                  f"From:            {res[0][4]} To {res[0][5]}\n"
                  f"Date of Journey: {d2}\n"
                  f"Departure Time:  {res[0][7]}\n"
                  f"Arrival Time:    {res[0][8]}\n"
                  "Passenger(s) Details:"
                  )
            passengers = []
            for i in range(len(res)):
                single_pass = []
                for j in range(5):
                    single_pass.append(res[i][j + 9])
                passengers.append(single_pass)
            print(tabulate(passengers,
                           headers=["Name", "Age", "Sex", "Class", "Status"],
                           tablefmt='simple_outline')
                  )
            time.sleep(3)


def cancel_bookings():
    userid = check_userid(shouldnot=True)
    check_mobileno(userid=userid, shouldnot=True)
    pnr = check_pnr()
    exists = database.check_if_exists('bookings', 'pnr', pnr, and_where={'userid': userid})
    if not exists:
        print(f"UserID: '{userid}' Does Not Have a Booking With PNR Number: '{pnr}'")
        return
    else:
        res = input("Are Your Sure You Want To Cancel This Booking? (Y/N): ")
        if res.strip().upper() == 'Y':
            database.cancel_booking(userid, pnr)
            print(f"\nSuccessfully Cancelled Booking For PNR Number: '{pnr}'")
        elif res.strip().upper() == 'N':
            print("\nCancellation Aborted!")
        else:
            print("Enter A Valid Option (Y/N): ")
