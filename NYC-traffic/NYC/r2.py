#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2. Trafico medio por hora del dia.

import sys
import operator

dates = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    date = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)
    aux_dates = []
    # If date is already a key in the dict
    if dates.has_key(date):
        counter = 0
        # Saving every value per hour and number of days
        for data in row:
            aux_dates.append(dates.get(date)[counter] + data)
            counter = counter + 1
        aux_dates.append(dates.get(date)[counter] + 1)
        dates[date] = aux_dates
    # If not, create the key in the dictionary
    else:
        # store every value per hour and number of dates
        for data in row:
            aux_dates.append(data)
        aux_dates.append(1)
        dates[date] = aux_dates

# Calculate median of every hour of a date / number of days
for date in dates:
    aux_dates = []
    for data in range(0, (len(dates.get(date)) - 1)):
        aux_dates.append(dates.get(date)[data] / dates.get(date)[-1])
    dates[date] = aux_dates

# Order dates
sorted_dates = sorted(dates.items(), key=operator.itemgetter(0), reverse=True)

# print date and the median of every hour of that date
for date in sorted_dates:
    # TODO: PREGUNTAR SI HACE FALTA ÍNDICE PARA LA REPRESENTACIÓN DE LOS DATOS
    print date[0] + ' ' + str(date[1])