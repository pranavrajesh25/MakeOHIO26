import requests
import time
import math

BUS_MAX_CAPACITY = 65
API_URL = "https://content.osu.edu/v2/bus/routes/"
ROUTES = ["CLS", "BE", "CC", "ER", "MC", "NWC"]

def reset_bus_data():
    with open("bus_management/bus_data.csv", "w") as bus_data:
        bus_data.write("")

        # Write header
        bus_data.writelines(["Route, Id, Stop1, Stop2, Stop3, Riders"])

def write_to_data(route, id, stop1, stop2, stop3, riders):
    with open("bus_management/bus_data.csv", "w") as bus_data:
        bus_data.writelines([route, id, stop1, stop2, stop3, riders])

def query_buses():
    for route in ROUTES:
        response = requests.get(API_URL + route + "/vehicles")
        if response.status_code == 200:
            print("Successful request")
            bus_info = response.json()["data"]["vehicles"]
            for bus in bus_info:
                print(bus["id"])
                print(bus["routeCode"])
        else:
            print(f"Request failed, status code: {response.status_code}")

    print()


reset_bus_data()
query_buses()