#!/usr/bin/python
# -*- coding: utf-8 -*-
# 4. Hora del dia con mas trafico por calle.

import sys

# TODO: PREGUNTAR SI TAMBIEN HAY QUE TENER EN CUENTA DATE

streets = {}
primera_linea = True
firstLine = None
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    if primera_linea:
        firstLine = row
        primera_linea = False
    else:
        # Data processing
        street = row.pop(0)

        # Changing list elements data type from string to int
        row = map(int, row)
        aux_streets = []

        # If street name is already a key in the dict, add sum of row's elements to its existing value
        if streets.has_key(street):
            counter = 0
            # Saving every value per hour
            for data in row:
                aux_streets.append(streets.get(street)[counter] + data)
                counter = counter + 1
            streets[street] = aux_streets

        # If not, create the key in the dictionary and store sum of row as it's value
        else:
            # Saving every value per hour
            for data in row:
                aux_streets.append(data)
            streets[street] = aux_streets


for street in streets:
    # Highest traffic per hour in a given street
    value = max(streets.get(street))
    # Hour
    index = streets.get(street).index(max(streets.get(street)))

    # Printing name of street, hour range and value
    print street + ' ' + str(firstLine[index]) + ' ' + str(value)