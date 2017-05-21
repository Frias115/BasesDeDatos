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
    row[-1] = row[-1].rstrip()

    if primera_linea:
        firstLine = row
        primera_linea = False
    else:
        # Data processing
        street = row.pop(0)

        row = map(int, row)
        aux_streets = []

        if streets.has_key(street):

            counter = 0
            for data in row:
                aux_streets.append(streets.get(street)[counter] + data)
                counter = counter + 1
            streets[street] = aux_streets

        else:
            for data in row:
                aux_streets.append(data)
            streets[street] = aux_streets


for street in streets:

    value = max(streets.get(street))
    index = streets.get(street).index(max(streets.get(street)))

    print street + ' ' + str(firstLine[index]) + ' ' + str(value)