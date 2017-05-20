#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2. Trafico medio por hora del dia.

import sys
import operator

dates = {}
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    row[-1] = row[-1].rstrip()

    # Data processing
    date = row.pop(0)

    row = map(int, row)
    aux_dates = []
    if dates.has_key(date):
        counter = 0
        for data in row:
            aux_dates.append(dates.get(date)[counter] + data)
            counter = counter + 1
        aux_dates.append(dates.get(date)[counter] + 1)
        dates[date] = aux_dates
    else:
        for data in row:
            aux_dates.append(data)
        aux_dates.append(1)
        dates[date] = aux_dates

for date in dates:
    aux_dates = []
    for data in range(0, (len(dates.get(date)) - 1)):
        aux_dates.append(dates.get(date)[data] / dates.get(date)[-1])
    dates[date] = aux_dates

sorted_dates = sorted(dates.items(), key=operator.itemgetter(0), reverse=True)

for date in sorted_dates:
    # TODO: PREGUNTAR SI HACE FALTA ÍNDICE PARA LA REPRESENTACIÓN DE LOS DATOS
    print date[0] + ' ' + str(date[1])