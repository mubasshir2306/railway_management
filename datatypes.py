from collections import namedtuple

Train = namedtuple("Train", "train_no train_name source_station_name destination_station_name")

TrainDist = namedtuple("TrainDist", "train_no train_name departure_time arrival_time dist")

StationData = namedtuple("StationData", "station_code station_name")

Fares = namedtuple("Fares", "train_no train_name first_ac second_ac third_ac sleeper")
