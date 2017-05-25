#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2. Trafico medio por hora del dia.

import sys
import operator

current_date = None
acc_traffic = []

data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    date = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)

    # Operating for every equal date
    if current_date == date:
        counter = 0
        # Saving every value per hour and number of days
        for data in row:
            acc_traffic[counter] = acc_traffic[counter] + data
            counter = counter + 1
        # Accumulating nº of days that are the same
        acc_traffic[counter] = acc_traffic[counter] + 1

    # If date changes
    else:
        # And it's not the first line
        if current_date is not None:
            print current_date + ',',

            # Printing nº of hours / total equal days
            for element in range(0,(len(acc_traffic) - 2)):
                print str(acc_traffic[element] / acc_traffic[-1]) + ',',

            # Printing last element so ',' does not print
            print str(acc_traffic[-2] / acc_traffic[-1])

        # Reset variables for next street
        current_date = date
        acc_traffic = []
        for data in row:
            acc_traffic.append(data)
        acc_traffic.append(1)

