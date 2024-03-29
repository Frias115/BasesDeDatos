#!/usr/bin/python
# -*- coding: utf-8 -*-
# 4. Hora del dia con mas trafico por calle.

import sys

current_street = None
acc_traffic = []

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
            # calculate highest traffic per hour in a given street
            value = max(acc_traffic)
            # Hour
            index = acc_traffic.index(value)

            # Printing name of street, hour range and value
            print current_street + ',' + str(index) + ':00-' + str(index + 1) + ':00,' + str(value)

        # Resetting variables for next street
        current_street = street
        acc_traffic = []
        for data in row:
            acc_traffic.append(data)


