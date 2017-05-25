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

    if current_street == street:
        acc_traffic = acc_traffic + int(row[0])

    else:
        if current_street is not None:
            print current_street + ',' + str(acc_traffic)

        current_street = street
        acc_traffic = int(row[0])

