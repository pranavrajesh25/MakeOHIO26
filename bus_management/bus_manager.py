import requests
import time
import math
import random

BUS_MAX_CAPACITY = 65
API_URL = "https://content.osu.edu/v2/bus/routes/"
ROUTES = ["CLS", "BE", "CC", "ER", "MC", "NWC"]

def reset_bus_data():
    with open("bus_management/bus_data.csv", "w") as bus_data:
        bus_data.write("")

        # Write header
        bus_data.writelines(["Route, Id, Stop1, Stop2, Stop3, Riders\n"])

def write_to_data(route, id, stop1, stop2, stop3, riders):
    with open("bus_management/bus_data.csv", "a") as bus_data:
        bus_data.writelines([route+","+id+","+stop1+","+stop2+","+stop3+","+riders+"\n"])

def query_buses():
    for route in ROUTES:
        response = requests.get(API_URL + route + "/vehicles")
        if response.status_code == 200:
            print("Successful request")
            bus_info = response.json()["data"]["vehicles"]
            for bus in bus_info:
                write_to_data(
                    bus["routeCode"],
                    bus["id"],
                    bus["predictions"][0]["destination"],
                    bus["predictions"][1]["destination"],
                    bus["predictions"][2]["destination"],
                    str(round(random.Random().random()*100))
                )

        else:
            print(f"Request failed, status code: {response.status_code}")

    print()


# reset_bus_data()
# query_buses()
def create_stops():
    stops = {}

    for route in ROUTES:
        a = requests.get(API_URL + route).json()
        route_stops = a["data"]["stops"]
        for stop in route_stops:
            stops[stop["name"]] = 1

    with open("bus_management/stop_data.csv", "w") as f:
        f.write("")
    with open("bus_management/stop_data.csv", "a") as file:
        for stop in stops.keys():
            file.write(stop + ", 5\n")

create_stops()