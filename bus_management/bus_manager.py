import requests
import time
import random
import matplotlib.pyplot as ml
import numpy as np

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
    print("Starting queries")
    for route in ROUTES:
        response = requests.get(API_URL + route + "/vehicles")
        if response.status_code == 200:
            bus_info = response.json()["data"]["vehicles"]
            for bus in bus_info:
                write_to_data(
                    bus["routeCode"],
                    bus["id"],
                    bus["predictions"][0]["destination"],
                    bus["predictions"][1]["destination"],
                    bus["predictions"][2]["destination"],
                    str(round(random.Random().random()*100)) # Data will be gathered from onboard cameras in the future
                )

        else:
            print(f"Request failed, status code: {response.status_code}")
    print("Finished querying bus routes")

def generate_stop_data():
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
            n = round(random.Random().random() * 12) # Data will be collected from bus stop cameras in the future
            file.write(stop + f", {n}\n")

def get_bus_route(id):
    with open("bus_management/bus_data.csv", "r") as file:
        for line in file:
            if str(id) in line:
                return line[:line.index(",")]

def collect_data():
    reset_bus_data()
    query_buses()
    generate_stop_data()

def calculate_ridership() -> dict[int, list[int]]:
    capacities = {}
    with open("bus_management/bus_data.csv", "r") as file:
        for line in file:
            if "Route" in line:
                continue
            ind1 = line.find(",")
            ind2 = line.find(",", ind1+1)
            ind3 = line.find(",", ind2+1)
            ind4 = line.find(",", ind3+1)
            ind5 = line.find(",", ind4+1)

            id = int(line[ind1+1:ind2])
            route = line[0:ind1]
            current = int(line[ind5+1:])

            p1 = line[ind2+1:ind3]
            p2 = line[ind3+1:ind4]
            p3 = line[ind4+1:ind5]

            n1=0
            n2=0
            n3=0

            with open("bus_management/stop_data.csv", "r") as stops:
                for stop in stops:
                    if p1 in stop:
                        n1 = int(stop[stop.find(",")+2:stop.find("\n")+1])
                    if p2 in stop:
                        n2 = int(stop[stop.find(",")+2:stop.find("\n")+1])
                    if p3 in stop:
                        n3 = int(stop[stop.find(",")+2:stop.find("\n")+1])
            
            n1 = current + n1
            n2 = n1 + n2
            n3 = n2 + n3

            capacities[id] = [current, n1, n2, n3]
    
    return capacities

def graph_projected_ridership(ridership: dict[int, list[int]]):
    for bus in ridership.keys():
        ml.figure(bus)
        route = get_bus_route(bus)
        x = np.array([0,1,2,3])
        y = np.array(ridership[bus])
        ml.plot(x,y)
        
        x0 = np.linspace(0,3)
        y0 = x0*0 + BUS_MAX_CAPACITY
        ml.plot(x0,y0)
        ml.title(f"{route} Bus Number {bus}")
        ml.xlabel("Future Stops")
        ml.xticks([0,1,2,3])
        ml.ylabel("Riders")
        ml.ylim([0,BUS_MAX_CAPACITY+15])
        ml.legend("Projected Ridership", "Max Ridership")

    ml.show()

if __name__ == "__main__":
    # generate_stop_data()
    graph_projected_ridership(calculate_ridership())

    # while True:
    #     time.sleep(10)
    #     collect_data()
    #     projected_ridership = calculate_ridership()
    #     print(projected_ridership)
