import database
from psycopg2 import Error
from trainRelatedQueries import find_all_trains, show_fares, get_station_code, check_if_route_exists
from utils import check_mobileno, check_userid, check_name, check_age, check_sex, check_train_number, \
    check_station_code_with_train_no, generate_pnr, generate_ticket_no, get_date, get_class, check_date, \
    get_num_pass, get_passenger_details


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

    print(
        "\nSome Important Information Regarding Ticket Bookings:\n"
        "- You must be a Registered User.\n"
        "- A Registered User can Book Tickets for a Maximum of 5 Different Journeys.\n"
        "- A Ticket can be Booked 2 Months before the Actual Trip.\n"
        "- A Maximum of 5 Passengers can be Booked in One Ticket.\n"
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
    check_mobileno(userid=userid, shouldnot=True)
    train_no = check_train_number()
    start_station_code = check_station_code_with_train_no(train_no, 'Starting')
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
            passenger = get_passenger_details()
            status = 'CNF'
            database.book_ticket(ticket_no, userid, pnr, train_no, start_station_code, end_station_code, date,
                                 departure_time, arrival_time, passenger[0], passenger[1], passenger[2], class_name,
                                 status)
            print(f"Passenger {num+1} added successfully!")

        print(f"\nTicket Booked!")
        print(f"Your PNR is: {pnr}")




