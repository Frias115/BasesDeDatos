#!/usr/bin/python
# -*- coding: utf-8 -*-
# 3. Calle con mas trafico y trafico total.

import sys
import operator

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

sorted_streets = sorted(streets.items(), key=operator.itemgetter(1), reverse=True)

print sorted_streets[0][0] + ' ' + str(sorted_streets[0][1])
