#!/usr/bin/python
# -*- coding: utf-8 -*-
# 1. Trafico total por calle.

import sys

current_street = None
acc_traffic = 0

data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)

    # Accumulating traffic for every street
    if current_street == street:
        acc_traffic = acc_traffic + int(row[0])

    # If the street changes,
    else:
        # And it's not the first line
        if current_street is not None:
            # Print the current street and it's traffic
            print current_street + ',' + str(acc_traffic)

        # Reset variables for next street
        current_street = street
        acc_traffic = int(row[0])

