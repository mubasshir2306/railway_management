import database
from tabulate import tabulate
import time
from utils import check_train_number, check_if_station_code_exists, check_station_code_with_train_no


def find_all_trains():

    start = check_if_station_code_exists('Boarding')
    end = check_if_station_code_exists('Destination')
    print(f"Finding All Trains From {start} To {end}...")
    time.sleep(1)
    ans = database.show_all_trains(start, end)
    if ans:
        print('\n' + tabulate(ans,
                              headers=["Train Number", "Train Name", f"Departure time ({start})",
                                       f"Arrival time ({end})", f"Distance Between {start} and {end} (KMs)"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print(f"\nSorry, No Trains Found Connecting '{start}' and '{end}'. "
              f"Please check Station Codes or search for Trains from Different Stations.\n")


def get_train_info_by_train_no():
    train_no = check_train_number()
    train_data = database.show_train_info(train_no)
    print("Getting Train Info...")
    if train_data:
        print('\n' + tabulate(train_data,
                              headers=["Train No.", "Train Name", "Source Station Name", "Destination Station Name"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print("\nEnter a Correct Train Number!\n")


def show_fares():
    train_no = check_train_number()
    start = check_station_code_with_train_no(train_no)
    end = check_station_code_with_train_no(train_no)
    exists = check_if_route_exists(train_no, start, end)
    if exists:
        fares = database.get_fares(train_no, start, end)
        if fares:
            print(f"The Fares for Different Classes for Train Number: '{train_no}' are: ")
            print('\n' + tabulate(fares,
                                  headers=["Train No.", "Train Name", "First AC", "Second AC", "Third AC", "Sleeper"],
                                  tablefmt='heavy_outline') + '\n'
                  )
        else:
            print("\nPlease enter the correct data and try again.\n")


def get_station_code():
    city_name = input("Enter The City Name: ")
    station_code = database.get_station_code(city_name)
    if station_code:
        print('\n' + tabulate(station_code,
                              headers=["Station Code", "Station Name"],
                              tablefmt='heavy_outline') + '\n'
              )
    else:
        print("\nNo Station Found. Please check the spelling or search the web.\n")


def check_if_route_exists(train_no, start_station_code, end_station_code):
    does_route_exists = database.check_train_from_to_end(train_no, start_station_code, end_station_code)
    if not does_route_exists:
        print(f"\nTrain Number '{train_no}' Does Not Run From '{start_station_code}' To '{end_station_code}'\n"
              f"It Runs From '{end_station_code}' To '{start_station_code}'")
        return False
    else:
        return True
