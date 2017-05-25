#!/usr/bin/python
# -*- coding: utf-8 -*-
# 5. Calle que mas trafico aporta a Brodway y trafico total aportado.

import sys

current_street = None
acc_traffic = 0

max_street = None
max_traffic = 0

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
        # And current traffic is greater than previous maximum
        if acc_traffic > max_traffic:
            # Assign current values to maximum values
            max_street = current_street
            max_traffic = acc_traffic

        # Resetting variables for next street
        current_street = street
        acc_traffic = int(row[0])

print max_street + ',' + str(max_traffic)