#!/usr/bin/python
# -*- coding: utf-8 -*-
# 5. Calle que mas trafico aporta a Brodway y trafico total aportado.


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
        if streets.has_key(street):
            streets[street] = streets.get(street) + sum(row)
        else:
            streets[street] = sum(row)

sorted_streets = sorted(streets.items(), key=operator.itemgetter(1), reverse=True)

print sorted_streets[0][0] + ' ' + str(sorted_streets[0][1])
