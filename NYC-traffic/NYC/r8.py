#!/usr/bin/python
# 8. Sentido de cada calle con mas trafico y trafico total.

import sys

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila