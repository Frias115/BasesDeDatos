#!/usr/bin/python
# -*- coding: utf-8 -*-
# 8. Sentido de cada calle con mas trafico y trafico total.
# Por cada calle, sacar el sentido que tenga más tráfico y su tráfico total.

import sys

streets = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)
    direction = row.pop(0)

    row = map(int, row)

    aux_street = [0, 0, 0, 0]

    if streets.has_key(street):
        aux_street = streets[street]
        if direction == 'NB' or direction == 'WB':
            aux_street[0] = direction
            aux_street[1] = streets.get(street)[1] + sum(row)
        else:
            aux_street[2] = direction
            aux_street[3] = streets.get(street)[3] + sum(row)

    else:
        if direction == 'NB' or direction == 'WB':
            aux_street[0] = direction
            aux_street[1] = sum(row)
        else:
            aux_street[2] = direction
            aux_street[3] = sum(row)

    streets[street] = aux_street

# Por cada calle, sacar el sentido que tenga más tráfico y su tráfico total.

for street in streets:
    if streets[street][1] > streets[street][3]:
        print street + ' ' + streets[street][0] + ' ' + str(streets[street][1])
    else:
        print street + ' ' + streets[street][2] + ' ' + str(streets[street][3])
