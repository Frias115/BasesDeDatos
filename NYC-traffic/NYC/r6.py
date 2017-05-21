#!/usr/bin/python
# -*- coding: utf-8 -*-
# 6. Calle que mas trafico aporta a Brodway por franja de hora.

import sys
import operator

streets = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)
    aux_streets = []

    # If street name is already a key in the dict
    if streets.has_key(street):
        counter = 0
        # Saving every value per hour
        for data in row:
            aux_streets.append(streets.get(street)[counter] + data)
            counter = counter + 1
        streets[street] = aux_streets
    # If not, create the key in the dictionary
    else:
        # Saving every value per hour
        for data in row:
            aux_streets.append(data)
        streets[street] = aux_streets

# For every range of hours
for hour in (range(0, 24)):
    traffic = 0
    best_street = None
    # Collect the street with highest traffic at a given hour
    for street in streets:
        if streets[street][hour] > traffic:
            traffic = streets[street][hour]
            best_street = street
    # Printing hour and best street
    print  str(hour) + ':00-' + str(hour+1) + ':00 -> ' + best_street
