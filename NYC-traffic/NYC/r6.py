#!/usr/bin/python
# -*- coding: utf-8 -*-
# 6. Calle que mas trafico aporta a Brodway por franja de hora.

import sys
import operator

streets = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)
    to = row.pop(0)

    if to == "BROADWAY":

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


for hour in (range(0, 24)):
    traffic = 0
    best_street = None
    for street in streets:
        if streets[street][hour] > traffic:
            traffic = streets[street][hour]
            best_street = street
    print  str(hour) + ':00-' + str(hour+1) + ':00 -> ' + best_street
