#!/usr/bin/python
# 1. Trafico total por calle.

import sys

streets = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)

    row = map(int, row)
    if streets.has_key(street):
        streets[street] = streets.get(street) + sum(row)
    else:
        streets[street] = sum(row)

for street in streets:
    print street + ' ' + str(streets[street])
