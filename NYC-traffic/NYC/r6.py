#!/usr/bin/python
# -*- coding: utf-8 -*-
# 6. Calle que mas trafico aporta a Brodway por franja de hora.

import sys

primera_linea = True
firstLine = None

current_street = None
acc_traffic = []

# Setting 24 positions of lists to 0
current_streets = [0] * 24
max_traffic = [0] * 24

data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)

    # Operating for every equal street
    if current_street == street:
        counter = 0

        # Saving every value per hour and number of days
        for data in row:
            acc_traffic[counter] = acc_traffic[counter] + data
            counter = counter + 1

    # If street name changes
    else:
        # And it's not the first line
        if current_street is not None:
            for hour in range(24):
                # And current traffic per hour is greater than previous maximum per hour
                if max_traffic[hour] < acc_traffic[hour]:
                    # Assign current values to maximum values
                    max_traffic[hour] = acc_traffic[hour]
                    current_streets[hour] = current_street

        # Resetting variables for next street
        current_street = street
        acc_traffic = []
        for data in row:
            acc_traffic.append(data)

for hour in range(0,24):
    print current_streets[hour]
