from trainRelatedQueries import find_all_trains, get_train_info_by_train_no, show_fares, get_station_code
from userFunctions import create_user, book_tickets, show_booking, cancel_bookings


def main_menu():
    print("Welcome to Railway Booking Manager!\n")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\nPress 1 ==> Check Trains Between Stations.\n"
            "Press 2 ==> Get Train Information by Train Number.\n"
            "Press 3 ==> Check Fares From Boarding Station to Destination Station.\n"
            "Press 4 ==> Search Station Code by City Name.\n"
            "Press 5 ==> SignUp/Create New User.\n"
            "Press 6 ==> Book Tickets.\n"
            "Press 7 ==> Show Bookings.\n"
            "Press 8 ==> Cancel Bookings.\n"
            "Press X ==> Close\n"
            )

        n = input("Enter Your Choice: ")

        if n == '1':
            find_all_trains()
        elif n == '2':
            get_train_info_by_train_no()
        elif n == '3':
            show_fares()
        elif n == '4':
            get_station_code()
        elif n == '5':
            create_user()
        elif n == '6':
            book_tickets()
        elif n == '7':
            show_booking()
        elif n == '8':
            cancel_bookings()

    print("\nThankyou!\n")


if __name__ == "__main__":
    main_menu()
