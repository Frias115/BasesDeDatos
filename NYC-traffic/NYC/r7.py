#!/usr/bin/python
# -*- coding: utf-8 -*-
# 7. Diferencia entre el trafico total de entrada a Brodway frente al de salida.

import sys

from_broadway = 0
to_broadway = 0
data = sys.stdin.readlines()
for line in data:
    row = line.split(', ')
    row[-1] = row[-1].rstrip()

    # Data processing
    From = row.pop(0)
    To = row.pop(0)

    row = map(int, row)

    if To == "BROADWAY":
        to_broadway = to_broadway + sum(row)

    else:
        from_broadway = from_broadway + sum(row)


print to_broadway - from_broadway
