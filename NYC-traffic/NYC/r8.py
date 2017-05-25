#!/usr/bin/python
# -*- coding: utf-8 -*-
# 8. Sentido de cada calle con mas trafico y trafico total.
# Por cada calle, sacar el sentido que tenga más tráfico y su tráfico total.

import sys

current_street = None
acc_traffic_d1 = 0
direc = None
acc_traffic_d2 = 0

data = sys.stdin.readlines()
for line in data:
    row = line.split('ñ ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    street = row.pop(0)
    direction = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)

    # Operating for every equal date
    if current_street == street:
        # And direction is north or west
        if direction == 'NB' or direction == 'WB':
            # Setting values to operate
            direc = direction
            acc_traffic_d1 = acc_traffic_d1 + int(row[0])

        # If the direction is south or east
        else:
            acc_traffic_d2 = acc_traffic_d2 + int(row[0])

    # If date changes
    else:
        # And it's not the first line
        if current_street is not None:
            # And North or West traffic is greater than South or East traffic respectively
            if acc_traffic_d1 > acc_traffic_d2:
                print current_street + ',' + direc + ',' + str(acc_traffic_d1)
            # If South or East traffic is greater than North or West traffic:
            else:
                # And Direction of street is North
                if dir == 'NB':
                    print current_street + ',' + 'SB' + ',' + str(acc_traffic_d2)
                # If direction is East
                else:
                    print current_street + ',' + 'EB' + ',' + str(acc_traffic_d2)

        # Resetting variables for next street
        direc = None
        current_street = street
        if direction == 'NB' or direction == 'WB':
            acc_traffic_d1 = int(row[0])
            acc_traffic_d2 = 0
        else:
            acc_traffic_d1 = 0
            acc_traffic_d2 = int(row[0])