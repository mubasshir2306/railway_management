from trainRelatedQueries import find_all_trains, get_train_info_by_train_no, show_fares, get_station_code, \
    get_train_route_chart
from userFunctions import create_user, book_tickets, show_booking, cancel_bookings


def main_menu():
    print("\n\033[1;35mWelcome to Railway Booking Manager!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\n\033[1;36;4mMAIN MENU\033[0m\n"
            "\033[1mPress 1 ==> Book Tickets.\n"
            "Press 2 ==> Show Bookings.\n"
            "Press 3 ==> Sign Up (OR) Create New User.\n"
            "Press 4 ==> Cancel Bookings.\n"
            "Press 5 ==> Check Trains Between Stations.\n"
            "Press 6 ==> Check Fares From Boarding Station to Destination Station.\n"
            "Press 7 ==> Get Route Chart For A Train by Train Number.\n"
            "Press 8 ==> Get Station Code by City Name.\n"
            "Press 9 ==> Get Train Information by Train Number.\n"
            "\033[1;31mPress X ==> Close\033[0m\n"
            )

        n = input("\033[1mEnter Your Choice: \033[0m")

        if n.strip() == '1':
            book_tickets()
        elif n.strip() == '2':
            show_booking()
        elif n.strip() == '3':
            create_user()
        elif n.strip() == '4':
            cancel_bookings()
        elif n.strip() == '5':
            find_all_trains()
        elif n.strip() == '6':
            show_fares()
        elif n.strip() == '7':
            get_train_route_chart()
        elif n.strip() == '8':
            get_station_code()
        elif n.strip() == '9':
            get_train_info_by_train_no()

    print("\n\033[1;35mThankyou, Have A Great Day!\033[0m")


if __name__ == "__main__":
    main_menu()
