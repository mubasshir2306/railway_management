import database
from tabulate import tabulate
import time
from utils import check_train_number, check_if_station_code_exists, check_station_code_with_train_no


def find_all_trains():
    print("\n\033[1;35;4mWelcome To The 'Search All Trains' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO SEARCH ALL TRAINS.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    start = check_if_station_code_exists('Boarding')
    end = check_if_station_code_exists('Destination')
    print(f"\033[1;33mFinding All Trains From {start} To {end}...\033[0m")
    time.sleep(1)
    ans = database.show_all_trains(start, end)
    if ans:
        print('\n' + tabulate(ans,
                              headers=["Train Number", "Train Name", f"Departure time ({start})",
                                       f"Arrival time ({end})", f"Distance Between {start} and {end} (KMs)"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print(f"\n\033[1;31mSorry, No Trains Found Connecting '{start}' and '{end}'.\033[0m"
              f"\033[1;31mPlease check Station Codes or search for Trains from Different Stations.\033[0m\n")


def get_train_info_by_train_no():
    print("\n\033[1;35;4mWelcome To The 'Get Train Information' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO GET TRAIN INFORMATION.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    train_no = check_train_number()
    train_data = database.show_train_info(train_no)
    print("\033[1;33mGetting Train Info...\033[0m")
    if train_data:
        print('\n' + tabulate(train_data,
                              headers=["Train No.", "Train Name", "Source Station Name", "Destination Station Name"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print("\n\033[1;31mEnter a Correct Train Number!\033[0m\n")


def show_fares():
    print("\n\033[1;35;4mWelcome To The 'Show Fares' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO SHOW FARES FOR A JOURNEY.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    train_no = check_train_number()
    start = check_station_code_with_train_no(train_no, "Boarding")
    end = check_station_code_with_train_no(train_no, "Destination")
    exists = check_if_route_exists(train_no, start, end)
    if exists:
        fares = database.get_fares(train_no, start, end)
        if fares:
            print(f"\n\033[1;32mThe Fares for Different Classes for Train Number: '{train_no}' are: \033[0m")
            print('\n' + tabulate(fares,
                                  headers=["Train No.", "Train Name", "First AC", "Second AC", "Third AC", "Sleeper"],
                                  tablefmt='heavy_outline') + '\n'
                  )
        else:
            print("\n\033[1;31mPlease enter the correct data and try again.\033[0m\n")


def get_station_code():
    print("\n\033[1;35;4mWelcome To The 'Find Station Code' Section!\033[0m")
    n = "no_op"
    while n.upper().strip() != 'X':
        print(
            "\033[1;34mPress X ==> CONTINUE TO FIND STATION CODE BY CITY NAME.\033[0m\n"
            "\033[1;31mPress E ==> Return To Main Menu.\033[0m\n"
        )
        n = input("Enter Your Choice: ")
        if n.strip().upper() == 'E':
            return

    city_name = input("Enter The City Name: ")
    station_code = database.get_station_code(city_name)
    if station_code:
        print('\n' + tabulate(station_code,
                              headers=["Station Code", "Station Name"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print("\n\033[1;31mNo Station Found. Please check the spelling or search the web.\033[0m")


def check_if_route_exists(train_no, start_station_code, end_station_code):
    does_route_exists = database.check_train_from_to_end(train_no, start_station_code, end_station_code)
    if not does_route_exists:
        print(f"\n\033[1;31mTrain Number '{train_no}' Does Not Run From '{start_station_code}' To '{end_station_code}'\033[0m\n"
              f"\033[1;31mIt Runs From '{end_station_code}' To '{start_station_code}'\033[0m")
        return False
    else:
        return True
