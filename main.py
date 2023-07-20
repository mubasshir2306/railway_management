import time
from trainRelatedQueries import find_all_trains, get_train_info_by_train_no, show_fares, get_station_code
from userFunctions import create_user, book_tickets

# def time_delay():
#     time.sleep(2)


def main_menu():
    print("Welcome to Railway Booking Manager!\n")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\nENTER THE NUMBER NEXT TO THE GIVEN OPTIONS TO ACCESS THEM:\n"
            "1. Check trains between stations.\n"
            "2. Get train info by Train Number.\n"
            "3. Check Fares from starting station to destination station.\n"
            "4. Search station code by city name.\n"
            "5. SignUp/Create New User.\n"
            "6. Book Tickets.\n"
            "X. Close\n"
            )

        n = input("Enter your choice: ")

        if n == '1':
            print("Choice 1 selected")
            find_all_trains()
            # time_delay()
        elif n == '2':
            get_train_info_by_train_no()
            # time_delay()
        elif n == '3':
            show_fares()
            # time_delay()
        elif n == '4':
            get_station_code()
            # time_delay()
        elif n == '5':
            create_user()
        elif n == '6':
            book_tickets()

    print("\nThankyou!\n")


if __name__ == "__main__":
    main_menu()
