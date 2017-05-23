#!/usr/bin/python
# -*- coding: utf-8 -*-
# 7. Diferencia entre el trafico total de entrada a Brodway frente al de salida.

import sys

from_broadway = 0
to_broadway = 0
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    # Stripping away \n character from last element in row
    row[-1] = row[-1].rstrip()

    # Data processing
    From = row.pop(0)
    To = row.pop(0)

    # Changing list elements data type from string to int
    row = map(int, row)

    # If traffic goes to Broadway, accumulate it's value
    if To == "BROADWAY":
        to_broadway = to_broadway + sum(row)
    # If traffic comes from Broadway, accumulate it's value
    else:
        from_broadway = from_broadway + sum(row)

# Difference between traffic entering Broadway and leaving Broadway
print to_broadway - from_broadway
