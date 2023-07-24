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
    print("\n\033[1;35;4mWelcome To The 'Sign Up' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO CREATE USER.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    userid = check_userid()
    fullname = check_name()
    mobileno = check_mobileno()
    age = check_age()
    sex = check_sex()

    try:
        database.create_user(userid, fullname, mobileno, age, sex)
        print("\n\033[1;32mUser Created Successfully!\033[0m\n")
    except Error:
        print(f"\n\033[1;31mAn error occurred, Please try again later.\033[0m\n")


def book_tickets():
    print(
        "\n\033[1;33;4mSome Important Information Regarding Ticket Booking:\033[0m\n"
        "\033[1m- You Must be a Registered User.\n"
        "- A Registered User can Book Tickets for a Maximum of 5 Different Journeys.\n"
        "- A Ticket can be Booked 3 Months before the Actual Trip.\n"
        "- A Maximum of 5 Passengers can be Booked in One Ticket.\n"
        "- Please make sure to know Train Number, Boarding Station Code and Destination "
        "Station Code before proceeding to Bookings.\033[0m\n"
        "\n\033[4mFollowing Options Might Help You:\033[0m"
    )

    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "Press 1 ==> Check Trains.\n"
            "Press 2 ==> Check Fares.\n"
            "Press 3 ==> Know Station Codes.\n"
            "Press 4 ==> To Sign Up (OR) Create New User.\n"
            "\033[1;34mPress X ==> CONTINUE TO BOOKING.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip() == '1':
            find_all_trains()
        elif n.strip() == '2':
            show_fares()
        elif n.strip() == '3':
            get_station_code()
        elif n.strip() == '4':
            create_user()
        elif n.strip().upper() == 'E':
            return

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
                print(f"\033[1;32mPassenger {num + 1} Added Successfully!\033[0m")

            print(f"\n\033[1;32mTicket Booked!\033[0m")
            print(
                f"Your PNR Number is: \033[1;33m{pnr}\033[0m\n"
                "Please Note Down Your PNR Number as it is Used to Check Bookings and Cancel Bookings.\n"
            )
    else:
        print("\033[1;31mCannot Proceed with Booking. Maximum Booking Limit Reached!\033[0m\n")
        return


def show_booking():
    print("\n\033[1;35;4mWelcome To The 'Show Booking' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO SEARCH FOR A BOOKING.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    userid = check_userid(shouldnot=True)
    check_mobileno(userid=userid, shouldnot=True)
    print(f"Press ==> 1: To Get All PNR Number for UserID: '{userid}'\n"
          "Press ==> 2: If You Know The PNR Number for the Booking and Continue to Show Booking.")
    while True:
        n = input("Enter Your Choice: ")
        if n == '1':
            res = database.get_all_pnr(userid)
            if not res:
                print(f"\033[1;31mUserID: '{userid}' Does Not Have Any Bookings!\033[0m")
                return
            else:
                print(f"All PNR Number for UserId: '{userid}' Are: ")
                for r in res:
                    print(r[0])
                break
        elif n == '2':
            break
        else:
            print("\033[1;33mPlease Enter A Valid Response!\033[0m")
    pnr = check_pnr()
    exists = database.check_if_exists('bookings', 'pnr', pnr, and_where={'userid': userid})
    if not exists:
        print(f"\033[1;31mUserID: '{userid}' Does Not Have a Booking With PNR Number: '{pnr}'\033[0m")
        return
    else:
        res = database.show_booking(userid, pnr)
        if not res:
            print("\033[1;31mNo Bookings Found!\033[0m")
        else:
            date = res[0][6]
            d1 = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            d2 = d1.strftime("%d-%m-%Y")
            now = datetime.datetime.today().date()
            print('\n')
            if d1 < now:
                print("\033[1;31mThis Booking Has Expired!\033[0m")
            print(
                  "\033[4mTICKET DETAILS\033[0m:\n"
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
            print('\n')
            time.sleep(3)


def cancel_bookings():
    print("\n\033[1;35;4mWelcome To The 'Cancel Booking' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO CANCEL A BOOKING.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    userid = check_userid(shouldnot=True)
    check_mobileno(userid=userid, shouldnot=True)
    pnr = check_pnr()
    exists = database.check_if_exists('bookings', 'pnr', pnr, and_where={'userid': userid})
    if not exists:
        print(f"\033[1;31mUserID: '{userid}' Does Not Have a Booking With PNR Number: '{pnr}'\033[0m")
        return
    else:
        res = input("\033[1;33mAre Your Sure You Want To Cancel This Booking? (Y/N):\033[0m ")
        if res.strip().upper() == 'Y':
            database.cancel_booking(userid, pnr)
            print(f"\n\033[1;32mSuccessfully Cancelled Booking For PNR Number: '{pnr}'\033[0m")
        elif res.strip().upper() == 'N':
            print("\n\033[1;32mCancellation Aborted!\033[0m")
        else:
            print("\033[1;33mEnter A Valid Option (Y/N):\033[0m ")
