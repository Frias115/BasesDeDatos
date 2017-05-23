#!/usr/bin/python
# -*- coding: utf-8 -*-
# 3. Calle con mas trafico y trafico total.

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

    # If street name is already a key in the dict, add sum of row's elements to its existing value
    if streets.has_key(street):
        streets[street] = streets.get(street) + sum(row)
    # If not, create the key in the dictionary and store sum of row as it's value
    else:
        streets[street] = sum(row)

# Sort results to get street with most traffic
sorted_streets = sorted(streets.items(), key=operator.itemgetter(1), reverse=True)

# print street name and result
print sorted_streets[0][0] + ' ' + str(sorted_streets[0][1])
