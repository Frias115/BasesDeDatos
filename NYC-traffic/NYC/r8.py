#!/usr/bin/python
# -*- coding: utf-8 -*-
# 8. Sentido de cada calle con mas trafico y trafico total.
# Por cada calle, sacar el sentido que tenga más tráfico y su tráfico total.

import sys

streets = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)
    direction = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)

    # Creating list to store direction 1, traffic of direction 1, direction 2, traffic of direction 2
    aux_street = [0, 0, 0, 0]

    # If street name is already a key in the dict
    if streets.has_key(street):
        aux_street = streets[street]
        # Differentiating street based on direction
        if direction == 'NB' or direction == 'WB':
            aux_street[0] = direction
            aux_street[1] = streets.get(street)[1] + sum(row)
        else:
            aux_street[2] = direction
            aux_street[3] = streets.get(street)[3] + sum(row)

    # If not, create the key in the dictionary
    else:
        # Differentiating street based on direction
        if direction == 'NB' or direction == 'WB':
            aux_street[0] = direction
            aux_street[1] = sum(row)
        else:
            aux_street[2] = direction
            aux_street[3] = sum(row)

    streets[street] = aux_street

for street in streets:
    # Checks which street direction has more traffic and prints it's information
    if streets[street][1] > streets[street][3]:
        print street + ' ' + streets[street][0] + ' ' + str(streets[street][1])
    else:
        print street + ' ' + streets[street][2] + ' ' + str(streets[street][3])
