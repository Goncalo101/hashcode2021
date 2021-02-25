#!/usr/bin/python

import sys
from tqdm import tqdm
import random
import math


class Street:
    def __init__(self, start, end, name, time):
        self.start = int(start)
        self.end = int(end)
        self.name = name
        self.time = int(time)

    def __repr__(self):
        return f'{self.name}: {self.start}-{self.end} travel time: {self.time}'


class Car:
    def __init__(self, _id, n_streets, streets: dict):
        self._id = _id
        self.n_streets = n_streets
        self.streets = streets

    def __repr__(self):
        return f'{self._id}: {self.streets}'


solution = {
    "intersections": [1, 0, 2, 3],
    "schedule": {
        "1": [["rue-d-athenes", 2], ["rue-d-amsterdam", 1]],
        "0": [["rue-de-londres", 2]],
        "2": [["rue-de-moscou", 1]],
        "3": [["rue-de-rome", 1]]}

}


def solve():
    solution = {
        "intersections":  [],
        "schedule": {}
    }

    car_map = {}
    for car in cars:
        for street in car.streets:
            try:
                car_map[street].append(car._id)
            except KeyError:
                car_map[street] = []
                car_map[street].append(car._id)

    for idx in range(n_intersections):
        i = 0
        for street in intersections[str(idx)]:
            try:
                n_cars = len(car_map[street])
                try:
                    solution["schedule"][str(idx)].append([street, n_cars])
                except KeyError:
                    solution["schedule"][str(idx)] = []
                    solution["schedule"][str(idx)].append([street, n_cars])
                i += 1
            except KeyError:
                continue

        if i > 0:
            solution["intersections"].append(idx)
        i = 0


    return solution

# [0, 0 ,1] -- 5 -> 2
def calc_current_time(time, times):
    length = len(times)
    while True:
        if time / length > 1:
            time /= length
        else:
            break
    return times[math.floor(time)-1]


def score(solution):
    time, score = 0, 0

    for car in cars:
        count = 0
        time = 0
        for street_name, street in car.streets.items():

            if count != 0:
                time += street.time

            count += 1
            if solution['schedule'].get(str(street.end)) != None and len(solution['schedule'][str(street.end)]) > 1:

                # Make times [0, 0, 1]
                times = []
                for i in range(len(solution['schedule'][str(street.end)])):
                    for j in range(solution['schedule'][str(street.end)][i][1]):
                        times.append(i)

                # Loop until dest
                while True:
                    curr = calc_current_time(time, times)
                    # print(calc_current_time(time, times))

                    current_street = solution['schedule'][str(street.end)][curr]
                    # print(current_street, street_name)

                    if current_street[0] == street_name:
                        break
                    time += 1
            else:
                pass
        if time <= sim_duration:
            score += bonus_points + (sim_duration - time)
        print(f'Score: {score}')
    return score


# main
with open(f'input/{sys.argv[1]}.txt', 'r') as input_file:
    sim_duration, n_intersections, n_streets, n_cars, bonus_points = map(
        int, input_file.readline().split())

    # Street
    streets = {}
    intersections = {}
    for i in range(n_streets):
        start, end, name, time = input_file.readline().split()

        try:
            if name not in set(intersections[end]):
                intersections[end].append(name)
        except KeyError:
            intersections[end] = []
            intersections[end].append(name)

        streets[name] = Street(start, end, name, time)
        # streets.append(Street(start, end, name, time))

    # Cars
    cars = []
    for i in range(n_cars):
        n_car_streets, car_streets = input_file.readline().split(maxsplit=1)
        _streets = {}
        for street in car_streets.split():
            _streets[street] = streets[street]

        cars.append(Car(i, n_car_streets, _streets))

# final_score = score(solution)
solution = solve()
with open(f'{sys.argv[1]}.out', 'w') as output_file:
    output_file.write(str(len(solution["intersections"])) + "\n")

    for k, v in solution["schedule"].items():
        output_file.write(f"{k}\n")
        output_file.write(f"{len(v)}\n")
        for value in v:
            output_file.write(f"{value[0]} {value[1]}\n")
