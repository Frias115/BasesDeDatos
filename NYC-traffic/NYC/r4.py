#!/usr/bin/python
# 4. Hora del dia con mas trafico por calle.

import sys

data = sys.stdin.readlines()
for line in data:
    fila = line.split(', ')
    fila[-1] = fila[-1].rstrip()
    print fila